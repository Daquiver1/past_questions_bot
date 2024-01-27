"""Serializer & Deserializer for Redis"""
import json
import re
from dateutil.parser import parse
from datetime import datetime
from redis.asyncio import Redis
from typing import Any, Dict


def custom_serializer(obj: Any) -> str:
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


async def store_data(redis_client: Redis, key: str, data: Any) -> None:  # noqa
    """Store data in Redis"""
    serialized_data = json.dumps(data, default=custom_serializer)
    await redis_client.set(key, serialized_data, ex=3600)


def custom_deserializer(dict_obj: Any) -> Dict[str, Any]:
    """Convert strings back to datetime objects where applicable"""
    for key, value in dict_obj.items():
        if isinstance(value, str) and re.match(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", value
        ):
            dict_obj[key] = parse(value)
    return dict_obj


async def get_data(redis_client: Redis, key: str) -> Any:  # noqa
    """Get data from Redis"""
    serialized_data = await redis_client.get(key)
    if serialized_data:
        return json.loads(
            serialized_data.decode("utf-8"), object_hook=custom_deserializer
        )
    return None
