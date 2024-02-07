"""Database Connect Tasks."""

from redis.asyncio import Redis

# Third party imports
from databases import Database
from fastapi import FastAPI

from src.core.config import DATABASE_URL, REDIS_URL


async def connect_to_db(app: FastAPI) -> None:
    """Connect to the SQLite database."""
    database = Database(DATABASE_URL)
    try:
        print("Connecting to SQLite database...")
        await database.connect()
        app.state._db = database
        print(f"Connected to SQLite database at {DATABASE_URL}")
    except Exception as e:
        print("Error connecting to SQLite database", e)


async def close_db_connection(app: FastAPI) -> None:
    """Close to postgres db."""
    try:
        await app.state._db.disconnect()
    except Exception as e:
        print("Error disconnecting from postgres", e)


async def connect_to_redis(app: FastAPI) -> None:
    """Connect to redis."""
    try:
        print("Connecting to redis database...")
        client = await Redis.from_url(REDIS_URL)
        app.state._redis = client
        print("Connected to redis database")
    except Exception as e:
        print("--- Redis Authentication Error")
        print(e)
        print("--- Redis Authentication Error")


async def close_redis_connection(app: FastAPI) -> None:
    """Connect to redis."""
    try:
        await app.state._redis.close()
        print("Disconnected from redis.asyncio database")
    except Exception as e:
        print("--- DB DISCONNECT ERROR ---")
        print(e)
        print("--- DB DISCONNECT ERROR ---")
