# VoiceGuard AI — SIH Deployment Guide

## 1. Local test
Backend:
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Frontend (new terminal):
```powershell
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## 2. GitHub
Create a GitHub repository and push this project. Do NOT commit `.venv`, `node_modules`, or `.env`.

## 3. Backend deployment (Render)
Create a Web Service from the GitHub repository.
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/api/health`

After deployment, copy the backend URL, e.g. `https://voiceguard-api.onrender.com`.
Set environment variable:
`FRONTEND_ORIGIN=https://YOUR-FRONTEND.vercel.app`

## 4. Frontend deployment (Vercel)
Import the GitHub repository.
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`

Set environment variable:
`VITE_API_URL=https://YOUR-BACKEND.onrender.com`

Redeploy. Open the Vercel URL.

## 5. SIH demo checklist
- Open the public frontend URL.
- Test audio upload.
- Test microphone permission over HTTPS.
- Open the incidents page and show the generated incident.
- Open the backend `/docs` URL if judges want to inspect APIs.

## Important technical disclosure
The included scoring layer is a deterministic prototype, not a trained voice-cloning classifier. For the SIH presentation, call it a prototype risk engine unless/until a trained anti-spoofing model is integrated and benchmarked.
