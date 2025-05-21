import time
import json
from fastapi import APIRouter
from app.config.config import settings
from app.config.redis_config import RedisBroker

router = APIRouter(prefix="/leaderboard")
redis_broker = RedisBroker()

@router.get("/")
async def get_leaderboard_score():
    # Fetch leaderboard from Redis using key leaderboard_data
    leaderboard_dt = redis_broker.redis_client.hgetall("leaderboard_data")
    leaderboard_data = {key: int(value) for key, value in leaderboard_dt.items()}
    return [{"player_id": player, "score": score} for player, score in leaderboard_data.items()]

@router.post("/update-score")
async def update_leaderboard_score(player_id: int, score: int):
    # Update the leaderboard data in Redis key leaderboard_data
    redis_broker.redis_client.hset("leaderboard_data", player_id, score)
    # Publish the score update
    data = {"player_id": player_id, "score": score}
    redis_broker.publish(settings.LEADERBOARD_REDIS_CHANNEL, data)
    return {"message": "Success"}

@router.get("/channels")
async def get_channels():
    # Get active channels
    active_channels = redis_broker.get_active_channels()
    return {"active_channels": active_channels}

@router.get("/listen/{channel}")
async def listen_channel(channel: str):
    # Listen to specified channel for 5 seconds
    messages = await redis_broker.listen_with_timeout(channel)
    return {"channel": channel, "messages": messages}

@router.post("/publish/{channel}")
async def publish_message(channel: str, message: dict):
    # Publish custom message to any channel
    subscribers = redis_broker.publish(channel, message)
    return {
        "channel": channel,
        "subscribers": subscribers,
        "message": message
    }