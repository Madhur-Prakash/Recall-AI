import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from recall_ai.src.quad_recall import quad_recall
from recall_ai.src.recall import recall
from voice_config.voice_api import voice
from recall_ai.helpers.utils import setup_logging

logger = setup_logging()

app = FastAPI(
    title="RecallAI API",
    description="API for RecallAI, a system for managing and retrieving information from images.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

app.include_router(recall, tags=["recall"])
app.include_router(quad_recall, tags=["quad_recall"])
app.include_router(voice, tags=["voice"])