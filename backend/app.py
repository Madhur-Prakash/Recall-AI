from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from recall_ai.src.recall import recall


# Load environment variables
load_dotenv()

# FastAPI app 
app = FastAPI(
    title="RecallAI API",
    description="API for RecallAI, a system for managing and retrieving information from images.",
    version="1.0.0",
    docs_url="/docs",  # Custom docs URL
    redoc_url="/redoc"  # Custom ReDoc URL
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

app.include_router(recall, tags=["recall"])

