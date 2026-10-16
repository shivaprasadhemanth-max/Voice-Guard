from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- PASTE THIS HERE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://voice-guard-chi.vercel.app",  # Your Vercel frontend URL
        "http://localhost:5173",                # For local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------

@app.get("/")
def read_root():
    return {"message": "API is running"}