import json
import redis
import time
from app.config.config import settings
from app.logger.logger import logger


# Enhanced RedisBroker class
class RedisBroker:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def publish(self, channel: str, data: dict):
        message = json.dumps(data)
        # Returns number of clients that received the message
        subscribers = self.redis_client.publish(channel, message)
        logger.info(f"Message sent to {subscribers} subscribers on channel {channel}")
        return subscribers

    def consume(self, channel: str):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        logger.info(f"Started consuming messages from channel: {channel}")

        try:
            for message in pubsub.listen():
                if message['type'] == 'message':
                    data = json.loads(message['data'])
                    logger.info(f"Received message on channel {channel}: {data}")
        except Exception as e:
            logger.error(f"Error in consumer: {str(e)}")
            pubsub.unsubscribe()


    def get_active_channels(self):
        # Use direct Redis command to get active channels
        return self.redis_client.execute_command('PUBSUB CHANNELS')

    async def listen_with_timeout(self, channel: str, timeout: int = 30):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(channel)
        messages = []

        start_time = time.time()
        while time.time() - start_time < timeout:
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                messages.append(json.loads(message['data']))
        pubsub.unsubscribe()
        return messages