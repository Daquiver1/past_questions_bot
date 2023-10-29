"""SqlLite user repository."""

from typing import Union

from db.repositories.base import BaseRepository
from models.user import UserCreate, UserInDb, UserPublic
from utils.uuid import generate_10_digit_uuid

CREATE_NEW_USER_QUERY = """
    INSERT INTO users (username, telegram_id, is_subscribed, is_eligible, balance,uuid)
    VALUES (:username, :telegram_id, :is_subscribed, :is_eligible, :balance, :uuid);
    """
DELETE_NEW_USER_QUERY = """
    DELETE FROM users
    WHERE telegram_id = :telegram_id
"""
GET_USER_BY_TELEGRAM_ID_QUERY = """
    SELECT *
    FROM users
    where telegram_id = :telegram_id;
"""

UPDATE_USER_IS_SUBSCRIBED_QUERY = """
    UPDATE users
    SET is_subscribed = :is_subscribed
    WHERE telegram_id = :telegram_id;
"""


UPDATE_USER_IS_ELIGIBLE_QUERY = """
    UPDATE users
    SET is_eligible = :is_eligible
    WHERE telegram_id = :telegram_id;
"""

UPDATE_USER_BALANCE_QUERY = """
    UPDATE users
    SET balance = :balance
    WHERE telegram_id = :telegram_id;
"""


class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def create_new_user(
        self, *, new_user: UserCreate
    ) -> Union[UserInDb, UserPublic, None]:
        uuid_ = generate_10_digit_uuid()

        """Create new user."""
        if await self.get_user_by_telegram_id(telegram_id=new_user.telegram_id):
            return None  # user exists
        await self.db.execute(
            query=CREATE_NEW_USER_QUERY, values={**new_user.dict(), "uuid": uuid_}
        )
        created_user = await self.get_user_by_telegram_id(
            telegram_id=new_user.telegram_id
        )
        return created_user

    async def delete_user(self, *, telegram_id: str) -> None:
        """Delete user."""
        if await self.get_user_by_telegram_id(telegram_id=telegram_id):
            return None
        await self.db.execute(
            query=DELETE_NEW_USER_QUERY, values={"telegram_id": telegram_id}
        )

    async def get_user_by_telegram_id(
        self, *, telegram_id: str
    ) -> Union[UserInDb, UserPublic, None]:
        """Get user by telegram id."""
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_TELEGRAM_ID_QUERY, values={"telegram_id": telegram_id}
        )
        if user_record:
            user = UserInDb(**user_record)  # type: ignore
            return user
        return None

    async def update_user_is_subscribed(
        self, *, value: int, telegram_id: str
    ) -> Union[UserInDb, UserPublic, None]:
        """Update users is subscribed."""
        await self.db.execute(
            query=UPDATE_USER_IS_SUBSCRIBED_QUERY,
            values={"is_subscribed": value, "telegram_id": telegram_id},
        )
        return await self.get_user_by_telegram_id(telegram_id=telegram_id)

    async def update_user_is_eligible(
        self, *, value: int, telegram_id: str
    ) -> Union[UserInDb, UserPublic, None]:
        """Update users is eligible."""

        await self.db.execute(
            query=UPDATE_USER_IS_ELIGIBLE_QUERY,
            values={"is_eligible": value, "telegram_id": telegram_id},
        )
        return await self.get_user_by_telegram_id(telegram_id=telegram_id)

    async def update_user_balance(
        self, *, value: int, telegram_id: str
    ) -> Union[UserInDb, UserPublic, None]:
        """Update users balance."""

        await self.db.execute(
            query=UPDATE_USER_BALANCE_QUERY,
            values={"balance": value, "telegram_id": telegram_id},
        )
        return await self.get_user_by_telegram_id(telegram_id=telegram_id)
