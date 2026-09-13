import json
import logging
import os
import redis

logger = logging.getLogger(__name__)

def get_redis_client():
    redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    try:
        return redis.Redis.from_url(redis_url, socket_timeout=2)
    except Exception as e:
        logger.warning(f"No se pudo conectar con Redis: {e}")
        return None

def publish_event(channel: str, data: dict):
    client = get_redis_client()
    if client:
        try:
            payload = json.dumps(data)
            client.publish(channel, payload)
            logger.info(f"Evento emitido en '{channel}': {data.get('event')}")
        except Exception as e:
            logger.error(f"Error publicando evento en '{channel}': {e}")
