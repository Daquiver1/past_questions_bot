"""DB repo for Users."""

# Standard library imports
from typing import Optional

from databases import Database

from src.db.repositories.base import BaseRepository
from src.models.users import UserCreate, UserInDB


ADD_USER_QUERY = """
    INSERT INTO users (username, first_name, last_name, telegram_id)
    VALUES (:username, :first_name, :last_name, :telegram_id)
    RETURNING username, first_name, last_name, telegram_id, created_At, updated_At;
"""

GET_USER_BY_TELEGRAM_ID_QUERY = """
    SELECT username, first_name, last_name, telegram_id, created_at, updated_at
    FROM users
    WHERE telegram_id = :telegram_id;
    """

GET_ALL_USERS_QUERY = """
    SELECT username, first_name, last_name, telegram_id, created_at, updated_at
    FROM users;
    """

DELETE_USER_BY_TELEGRAM_ID_QUERY = """
    DELETE FROM users
    WHERE telegram_id = :telegram_id
    RETURNING id;
"""


class UserRepository(BaseRepository):
    """All db actions associated with the user resource."""

    def __init__(self, db: Database) -> None:
        """Initialize db"""
        super().__init__(db)

    async def add_new_user(self, *, new_user: UserCreate) -> UserInDB:
        """Create new users data."""
        return await self.db.fetch_one(
            query=ADD_USER_QUERY,
            values=new_user.dict(),
        )

    async def get_all_users(self) -> list[UserInDB]:
        """Get all users data"""
        return await self.db.fetch_all(query=GET_ALL_USERS_QUERY)

    async def get_user_details(self, telegram_id: str) -> Optional[UserInDB]:
        """Get user data"""
        user = await self.db.fetch_one(
            query=GET_USER_BY_TELEGRAM_ID_QUERY,
            values={"telegram_id": telegram_id},
        )
        return user

    async def delete_user(self, *, telegram_id: str) -> str:
        """Delete user data by telegram_id."""
        return await self.db.execute(
            query=DELETE_USER_BY_TELEGRAM_ID_QUERY,
            values={"telegram_id": telegram_id},
        )
