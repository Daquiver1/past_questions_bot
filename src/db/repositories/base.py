"""Base Repository."""

# Third party imports
from databases import Database
from redis.asyncio import Redis


class BaseRepository:
    """Base class."""

    def __init__(self, db: Database, r_db: Redis) -> None:
        """Initialize. db (Database): Initialize database"""
        self.db = db
        self.r_db = r_db
