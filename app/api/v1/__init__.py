from urllib.response import addbase

from fastapi import APIRouter
from app.api.v1.routers import leaderboard

api_router = APIRouter(prefix='/api/v1')
api_router.include_router(leaderboard.router,tags=["Redis Leaderboard API"])