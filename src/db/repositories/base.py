"""Base Repository."""

# Third party imports
from databases import Database


class BaseRepository:
    """Base class."""

    def __init__(self, db: Database) -> None:
        """Initialize. db (Database): Initialize database"""
        self.db = db
