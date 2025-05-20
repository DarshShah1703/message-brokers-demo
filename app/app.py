import threading

from fastapi import FastAPI
from app.config.config import settings
from contextlib import asynccontextmanager

from app.config.redis_config import RedisBroker
from app.api.v1 import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=RedisBroker().consume, args={settings.LEADERBOARD_REDIS_CHANNEL})
    thread.start()  # Keeps the thread running as long as FastAPI app is running
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

