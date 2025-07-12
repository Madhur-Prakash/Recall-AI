import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from recall_ai.src.recall import recall
from recall_ai.helpers.dependencies import get_llm, get_embeddings_model, get_vectorstore
from recall_ai.helpers.utils import setup_logging
from contextlib import asynccontextmanager
import asyncio

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up RecallAI application...")
    start = time.time()
    logger.info(f"✅ Application started in {time.time() - start:.2f} seconds")

    # Start background warmup without blocking startup
    async def warmup():
        logger.info("Background warmup: Preloading models...")
        get_embeddings_model()
        get_llm()
        get_vectorstore()
        logger.info(f"✅ Background warmup complete in {time.time() - start:.2f} seconds")

    # Schedule warmup in the background (non-blocking)
    asyncio.create_task(warmup())

    yield

    logger.info("Shutting down RecallAI application...")


app = FastAPI(
    title="RecallAI API",
    description="API for RecallAI, a system for managing and retrieving information from images.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
