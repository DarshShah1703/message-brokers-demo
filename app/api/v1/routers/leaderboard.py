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

