from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone
import hashlib, math, random, time, os

app = FastAPI(title="VoiceGuard AI API", version="1.0.0")
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
allowed_origins = [x.strip() for x in frontend_origin.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

incidents = []

@app.get("/")
def root():
    return {"service": "VoiceGuard AI API", "status": "online", "docs": "/docs"}

class AnalyzeText(BaseModel):
    duration: float = 30
    transaction_value: float = 0
    caller_verified: bool = False

class VerifyAction(BaseModel):
    action: str
    incident_id: str


def score_features(duration: float, transaction_value: float, caller_verified: bool, seed: int = 0):
    # Prototype scoring layer. Replace these deterministic heuristics with CNN/Transformer inference.
    acoustic = 0.28 + ((seed % 17) / 100)
    prosody = 0.24 + (((seed // 7) % 19) / 100)
    consistency = 0.18 + (((seed // 13) % 21) / 100)
    context = min(0.35, transaction_value / 2000000) + (0.10 if not caller_verified else 0)
    risk = min(0.99, 0.35*acoustic + 0.30*prosody + 0.20*consistency + 0.15*context + (0.08 if duration < 8 else 0))
    return {
        "risk_score": round(risk * 100, 1),
        "acoustic_score": round(acoustic * 100, 1),
        "prosody_score": round(prosody * 100, 1),
        "consistency_score": round(consistency * 100, 1),
        "context_score": round(context * 100, 1),
        "classification": "HIGH RISK" if risk >= .70 else "SUSPICIOUS" if risk >= .45 else "LIKELY AUTHENTIC",
    }

@app.get("/api/health")
def health():
    return {"status":"ok", "service":"VoiceGuard AI", "time":datetime.now(timezone.utc).isoformat()}

@app.get("/api/dashboard")
def dashboard():
    high = sum(1 for x in incidents if x["risk_score"] >= 70)
    return {"total_calls": 1248 + len(incidents), "high_risk": 18 + high, "blocked": 7 + sum(1 for x in incidents if x.get("action")=="block"), "verified": 1168 + sum(1 for x in incidents if x["risk_score"] < 45), "incidents": incidents[-10:]}

@app.post("/api/analyze")
def analyze(data: AnalyzeText):
    seed = int(time.time() * 1000) % 100000
    result = score_features(data.duration, data.transaction_value, data.caller_verified, seed)
    incident_id = hashlib.sha1(f"{seed}-{data.duration}".encode()).hexdigest()[:10]
    event = {"id":incident_id, "timestamp":datetime.now(timezone.utc).isoformat(), **result, "action":"review"}
    incidents.append(event)
    return event

@app.post("/api/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(400, "Audio file is required")
    raw = await file.read()
    if len(raw) == 0:
        raise HTTPException(400, "Empty audio file")
    seed = int(hashlib.sha256(raw).hexdigest()[:8], 16)
    duration = max(1, min(180, len(raw) / 16000))
    result = score_features(duration, 0, False, seed)
    incident_id = hashlib.sha1(raw[:2048]).hexdigest()[:10]
    event = {"id":incident_id, "filename":file.filename, "timestamp":datetime.now(timezone.utc).isoformat(), **result, "action":"review"}
    incidents.append(event)
    return event

@app.post("/api/action")
def action(data: VerifyAction):
    for item in incidents:
        if item["id"] == data.incident_id:
            if data.action not in {"verify", "block", "callback", "mfa"}:
                raise HTTPException(400, "Invalid action")
            item["action"] = data.action
            return {"success": True, "incident": item}
    raise HTTPException(404, "Incident not found")

@app.get("/api/incidents")
def get_incidents():
    return list(reversed(incidents))
