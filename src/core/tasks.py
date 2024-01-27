"""Core task: Connect and Disconnect to db when application starts and stops."""

# Standard library imports
from typing import Callable

# Third party imports is right
from fastapi import FastAPI

from src.db.tasks import (
    close_db_connection,
    connect_to_db,
    connect_to_redis,
    close_redis_connection,
)


def create_start_app_handler(app: FastAPI) -> Callable:
    """
    It returns a function that connects to the database.

    Args:
      app (FastAPI): FastAPI

    Returns:
      A function that takes no arguments and returns None.
    """
    """Connect to db."""

    async def start_app() -> Callable:
        await connect_to_db(app)
        await connect_to_redis(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Disconnect db."""

    async def stop_app() -> None:
        await close_db_connection(app)
        await close_redis_connection(app)

    return stop_app
