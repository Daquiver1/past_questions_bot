"""Dependency for db."""

# Standard library imports
from typing import Callable, Type, Union

# Third party imports
from databases import Database
from fastapi import Depends
from redis.asyncio import Redis
from starlette.requests import Request

from src.db.repositories.base import BaseRepository


def get_database(request: Request) -> Database:
    """Get db from app state."""
    return request.app.state._db


def get_redis(request: Request) -> Redis:
    """Get redis from app state."""
    return request.app.state._redis


def get_repository(repo_type: Union[Type[BaseRepository], BaseRepository]) -> Callable:
    """Dependency for db."""

    def get_repo(
        db: Database = Depends(get_database), redis: Redis = Depends(get_redis)
    ) -> Type[BaseRepository]:
        return repo_type(db, redis)  # type: ignore

    return get_repo
