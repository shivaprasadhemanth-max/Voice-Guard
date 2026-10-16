from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI(title="VoiceGuard AI API")

@app.post("/api/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run your model inference:
    # verdict, confidence = run_voiceguard_inference(temp_path)
    os.remove(temp_path)
    
    return {"verdict": "Authentic", "confidence_score": 0.95, "filename": file.filename}