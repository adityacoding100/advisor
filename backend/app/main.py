from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(title="AI Financial Advisor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router, prefix="/api")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}