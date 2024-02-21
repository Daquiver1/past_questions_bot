"""Repository for subscriptions history."""

from typing import List, Optional

from databases import Database
from redis.asyncio import Redis
from src.db.repositories.subscriptions import SubscriptionRepository

from src.db.repositories.base import BaseRepository
from src.models.subscriptions_history import (
    SubscriptionHistoryCreate,
    SubscriptionHistoryInDB,
)

ADD_SUBSCRIPTION_HISTORY_QUERY = """
    INSERT INTO subscription_history (user_telegram_id, subscription_id, tier, amount, transaction_id, is_active, updated_at)
    VALUES (:user_telegram_id, :subscription_id, :tier, :amount, :transaction_id, :is_active, :updated_at)
    RETURNING id, user_telegram_id, subscription_id, tier, amount, transaction_id, is_active, created_at, updated_at;
    """

GET_SUBSCRIPTION_HISTORY_BY_USER_TELEGRAM_ID_QUERY = """
    SELECT id, user_telegram_id, subscription_id, tier, amount, transaction_id, is_active, created_at, updated_at
    FROM subscription_history
    WHERE user_telegram_id = :user_telegram_id;
    """

GET_SUBSCRIPTION_HISTORY_BY_SUBSCRIPTION_ID_QUERY = """
    SELECT id, user_telegram_id, subscription_id, tier, amount, transaction_id, is_active, created_at, updated_at
    FROM subscription_history
    WHERE subscription_id = :subscription_id;
    """

GET_ALL_SUBSCRIPTION_HISTORY_QUERY = """
    SELECT id, user_telegram_id, subscription_id, tier, amount, transaction_id, is_active, created_at, updated_at
    FROM subscription_history;
    """


class SubscriptionHistoryRepository(BaseRepository):
    """Repository for subscriptions history."""

    def __init__(self, db: Database, redis: Redis) -> None:
        """Initialize the repository."""
        super().__init__(db, redis)
        self.subscription_repo = SubscriptionRepository(db, redis)

    async def add_subscription_history(
        self, *, subscription_history_create: SubscriptionHistoryCreate
    ) -> Optional[SubscriptionHistoryInDB]:
        """Add subscription history to the database."""
        if not await self.subscription_repo.get_subscription_by_user_telegram_id(
            user_telegram_id=subscription_history_create.user_telegram_id
        ):
            return None
        subscription_history_create.tier = subscription_history_create.tier.tier_name
        subscription_history = await self.db.fetch_one(
            query=ADD_SUBSCRIPTION_HISTORY_QUERY,
            values=subscription_history_create.model_dump(),
        )
        if subscription_history:
            return SubscriptionHistoryInDB(**subscription_history)
        print("no subscription history.")
        return None

    async def get_all_subscription_history(self) -> list[SubscriptionHistoryInDB]:
        """Get all subscription history."""
        subscription_history = await self.db.fetch_all(
            query=GET_ALL_SUBSCRIPTION_HISTORY_QUERY,
        )
        return [SubscriptionHistoryInDB(**sub) for sub in subscription_history]

    async def get_all_subscription_history_by_user_telegram_id(
        self, *, user_telegram_id: int
    ) -> List[SubscriptionHistoryInDB]:
        """Get subscription history by user telegram id."""
        subscription_history = await self.db.fetch_all(
            query=GET_SUBSCRIPTION_HISTORY_BY_USER_TELEGRAM_ID_QUERY,
            values={"user_telegram_id": user_telegram_id},
        )
        return [SubscriptionHistoryInDB(**sub) for sub in subscription_history]

    async def get_all_subscription_history_by_subscription_id(
        self, *, subscription_id: int
    ) -> List[SubscriptionHistoryInDB]:
        """Get subscription history by subscription id."""
        subscription_history = await self.db.fetch_all(
            query=GET_SUBSCRIPTION_HISTORY_BY_SUBSCRIPTION_ID_QUERY,
            values={"subscription_id": subscription_id},
        )
        return [SubscriptionHistoryInDB(**sub) for sub in subscription_history]
