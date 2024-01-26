"""Database Connect Tasks."""

# Third party imports
from databases import Database
from fastapi import FastAPI

from src.core.config import DATABASE_URL


async def connect_to_db(app: FastAPI) -> None:
    """Connect to postgres db."""
    DB_URL = DATABASE_URL
    database = Database(str(DB_URL))
    try:
        print("Connecting to postgres database")
        await database.connect()
        app.state._db = database
        print(f"Connected to postgres database {DB_URL}")
    except Exception as e:
        print("Error connecting to postgres database", e)


async def close_db_connection(app: FastAPI) -> None:
    """Close to postgres db."""
    try:
        await app.state._db.disconnect()
    except Exception as e:
        print("Error disconnecting from postgres", e)
