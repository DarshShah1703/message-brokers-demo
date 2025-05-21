import threading

from fastapi import FastAPI
from app.config.config import settings
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.config.redis_config import RedisBroker
from app.api.v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=RedisBroker().consume, args={settings.LEADERBOARD_REDIS_CHANNEL,'leaderboard-test'})
    thread.start()  # Keeps the thread running as long as FastAPI app is running
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

