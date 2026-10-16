# VoiceGuard AI — End-to-End MVP

Prototype implementation based on the uploaded VoiceGuard AI PDOC.

## Architecture
- Frontend: React + Vite, responsive command-center dashboard, WebRTC microphone capture, audio upload, incident UI.
- Backend: FastAPI REST API.
- Detection pipeline: acoustic, prosody, cross-session consistency and contextual scoring interface. The current implementation uses a deterministic prototype scoring layer; replace `score_features()` with trained CNN/Transformer/Wav2Vec/LSTM/autoencoder inference for production.
- Actions: MFA, callback, block/hold, incident logging.
- Ready extension points: PostgreSQL/Redis/Elasticsearch, SMS/email, webhooks, SDKs, DID/blockchain audit.

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal (normally http://localhost:5173).

## Notes
Browser microphone access requires localhost or HTTPS. The MVP stores incidents in memory; restarting the backend clears them. For production, add authentication/RBAC, persistent storage, encrypted transport, model serving, real SMS/email providers, and compliance controls.
