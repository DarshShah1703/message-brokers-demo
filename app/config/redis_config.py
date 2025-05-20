import json
import redis

from app.config.config import settings
from app.logger.logger import logger


class RedisBroker:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True
        )

    def publish(self, channel: str, data: dict):
        message = json.dumps(data)
        # Publish the message to the channel
        self.redis_client.publish(channel, message)

    def consume(self, channel: str):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            logger.info(f"Consume message: {message}")
            if message and message["type"] == "message":
                logger.info(f"Received Redis Message From Consumer: {message['data']}")