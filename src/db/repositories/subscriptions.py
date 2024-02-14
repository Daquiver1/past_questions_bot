"""Repository for subscriptions."""

from typing import Optional

from databases import Database
from redis.asyncio import Redis

from src.db.repositories.base import BaseRepository
from src.db.repositories.subscriptions_history import SubscriptionHistoryRepository
from src.models.subscriptions import SubscriptionCreate, SubscriptionInDB
from src.models.subscriptions_history import SubscriptionHistoryCreate

UPSERT_SUBSCRIPTION_QUERY = """
    INSERT INTO subscriptions (user_telegram_id, tier, balance, transaction_id, is_active, updated_at)
    VALUES (:user_telegram_id, :tier, :balance, :transaction_id, :is_active, :updated_at)
    ON CONFLICT(user_telegram_id) DO UPDATE SET
        tier = excluded.tier,
        balance = subscriptions.balance + excluded.balance,  -- Add the incoming balance to the existing balance
        transaction_id = excluded.transaction_id,
        is_active = excluded.is_active,
        updated_at = excluded.updated_at;
"""


GET_SUBSCRIPTION_BY_USER_TELEGRAM_ID_QUERY = """
    SELECT id, user_telegram_id, tier, balance,is_active, transaction_id, created_at, updated_at
    FROM subscriptions
    WHERE user_telegram_id = :user_telegram_id;
    """
GET_SUBSCRIPTION_BY_TRANSACTION_ID_QUERY = """
    SELECT id, user_telegram_id, tier, balance, is_active,transaction_id, created_at, updated_at
    FROM subscriptions
    WHERE transaction_id = :transaction_id;
    """

GET_SUBSCRIPTION_BY_TIER_QUERY = """
    SELECT id, user_telegram_id, tier, balance, is_active,transaction_id, created_at, updated_at
    FROM subscriptions
    WHERE tier = :tier;
    """

GET_ALL_SUBSCRIPTIONS_QUERY = """
    SELECT id, user_telegram_id, tier, balance, is_active,transaction_id, created_at, updated_at
    FROM subscriptions;
    """

GET_ALL_ACTIVE_SUBSCRIPTIONS_QUERY = """
    SELECT id, user_telegram_id, tier, balance, is_active,transaction_id, created_at, updated_at
    FROM subscriptions
    WHERE is_active = True;
    """
UPDATE_SUBSCRIPTION_BALANCE_QUERY = """
    UPDATE subscriptions
    SET balance = :balance, is_active = :is_active
    WHERE user_telegram_id = :user_telegram_id"""

DELETE_SUBSCRIPTION_BY_USER_TELEGRAM_ID_QUERY = """
    DELETE FROM subscriptions
    WHERE user_telegram_id = :user_telegram_id
    RETURNING id;
    """


class SubscriptionRepository(BaseRepository):
    """All db actions associated with the subscription resource."""

    def __init__(self, db: Database, r_db: Redis) -> None:
        """Initialize db"""
        super().__init__(db, r_db)
        self.subscription_history_repo = SubscriptionHistoryRepository(db, r_db)

    async def upsert_new_subscription(
        self,
        *,
        new_subscription: SubscriptionCreate,
    ) -> Optional[SubscriptionInDB]:
        """Create new subscription data."""
        new_subscription.tier = new_subscription.tier.tier_name
        await self.db.fetch_one(
            query=UPSERT_SUBSCRIPTION_QUERY,
            values=new_subscription.dict(),
        )
        subscription = await self.get_subscription_by_user_telegram_id(
            new_subscription.user_telegram_id
        )
        if subscription:
            subscription_history_create = SubscriptionHistoryCreate(
                subscription_id=subscription.id,
                user_telegram_id=subscription.user_telegram_id,
                tier=subscription.tier,
                amount=subscription.balance,
                transaction_id=subscription.transaction_id,
                is_active=subscription.is_active,
            )
            await self.subscription_history_repo.add_subscription_history(
                subscription_history_create=subscription_history_create
            )
            return subscription
        return None

    async def get_subscription_by_user_telegram_id(
        self, user_telegram_id: int
    ) -> Optional[SubscriptionInDB]:
        """Get subscription data"""
        subscription = await self.db.fetch_one(
            query=GET_SUBSCRIPTION_BY_USER_TELEGRAM_ID_QUERY,
            values={"user_telegram_id": user_telegram_id},
        )
        if subscription:
            return SubscriptionInDB(**subscription)
        return None

    async def get_subscription_by_transaction_id(
        self, transaction_id: str
    ) -> Optional[SubscriptionInDB]:
        """Get subscription data"""
        subscription = await self.db.fetch_one(
            query=GET_SUBSCRIPTION_BY_TRANSACTION_ID_QUERY,
            values={"transaction_id": transaction_id},
        )
        if subscription:
            return SubscriptionInDB(**subscription)
        return None

    async def get_subscription_by_tier(self, tier: str) -> Optional[SubscriptionInDB]:
        """Get subscription data"""
        subscription = await self.db.fetch_one(
            query=GET_SUBSCRIPTION_BY_TIER_QUERY,
            values={"tier": tier},
        )
        if subscription:
            return SubscriptionInDB(**subscription)
        return None

    async def get_all_subscriptions(self) -> list[SubscriptionInDB]:
        """Get all subscriptions data"""
        subscriptions = await self.db.fetch_all(query=GET_ALL_SUBSCRIPTIONS_QUERY)
        return [SubscriptionInDB(**subscription) for subscription in subscriptions]

    async def get_all_active_subscriptions(self) -> list[SubscriptionInDB]:
        """Get all active subscriptions data"""
        subscriptions = await self.db.fetch_all(
            query=GET_ALL_ACTIVE_SUBSCRIPTIONS_QUERY
        )
        return [SubscriptionInDB(**subscription) for subscription in subscriptions]

    async def update_subscription_balance(
        self, user_telegram_id: int, new_balance: int
    ) -> Optional[SubscriptionInDB]:
        """Update subscription balance"""
        if new_balance < 0:
            raise ValueError("Balance cannot be less than 0")
        is_active = True
        subscription = await self.get_subscription_by_user_telegram_id(user_telegram_id)
        if not subscription:
            return None

        if subscription.balance - new_balance < 0:
            raise ValueError("New balance cannot be greater than old balance.")
        if subscription.balance - new_balance == 0:
            is_active = False

        await self.db.fetch_one(
            query=UPDATE_SUBSCRIPTION_BALANCE_QUERY,
            values={
                "user_telegram_id": user_telegram_id,
                "balance": new_balance,
                "is_active": is_active,
            },
        )
        return subscription

    async def delete_subscription_by_user_telegram_id(
        self, user_telegram_id: int
    ) -> int:
        """Delete subscription data"""
        return await self.db.execute(
            query=DELETE_SUBSCRIPTION_BY_USER_TELEGRAM_ID_QUERY,
            values={"user_telegram_id": user_telegram_id},
        )
        
