"""Serializer & Deserializer for Redis"""

import json
import re
from datetime import datetime
from typing import Any, Dict

from dateutil.parser import parse
from redis.asyncio import Redis

from src.models.past_question_filter_enum import PastQuestionFilter


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


async def invalidate_related_cache_entries(redis_client: Redis) -> None:
    """Invalidate all cache entries related to a specific past question ID."""
    filter_types = [
        PastQuestionFilter.PAST_QUESTION_ID.value,
        PastQuestionFilter.COURSE_CODE.value,
        PastQuestionFilter.COURSE_NAME.value,
        PastQuestionFilter.COURSE_TITLE.value,
        PastQuestionFilter.LECTURER_NAME.value,
        PastQuestionFilter.SEMESTER.value,
        PastQuestionFilter.YEAR.value,
    ]

    keys_to_invalidate = []
    for filter_type in filter_types:
        key_pattern = f"{filter_type}_*"
        keys = await redis_client.keys(key_pattern)
        decoded_keys = [key.decode("utf-8") for key in keys]
        keys_to_invalidate.extend(decoded_keys)

    unique_keys_to_invalidate = list(set(keys_to_invalidate))

    if unique_keys_to_invalidate:
        await redis_client.delete(*unique_keys_to_invalidate)
