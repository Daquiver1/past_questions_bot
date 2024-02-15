"""Subscription history repository test."""

import pytest
from databases import Database
from httpx import AsyncClient
from redis.asyncio import Redis

from src.db.repositories.subscriptions import SubscriptionRepository
from src.db.repositories.users import UserRepository
from src.models.subscriptions import SubscriptionCreate
from src.models.users import UserCreate
from src.db.repositories.subscriptions_history import SubscriptionHistoryRepository
from src.models.subscriptions_history import (
    SubscriptionHistoryCreate,
    SubscriptionHistoryInDB,
)

pytestmark = pytest.mark.asyncio


class TestSubscriptionHistoryRepo:
    """Subscription history repository test."""

    async def test_create_subscription_history(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_user: UserCreate,
        new_subscription: SubscriptionCreate,
        new_subscription_history: SubscriptionHistoryCreate,
    ) -> None:
        """Test creating a new subscription history."""
        db, r_db = await db, await r_db
        subscription_history_repo = SubscriptionHistoryRepository(db, r_db)
        await UserRepository(db, r_db).add_new_user(new_user=new_user)
        subscription = await SubscriptionRepository(db, r_db).upsert_new_subscription(
            new_subscription=new_subscription
        )
        new_subscription_history.subscription_id = subscription.id
        created_subscription_history = (
            await subscription_history_repo.add_subscription_history(
                subscription_history_create=new_subscription_history
            )
        )
        assert isinstance(created_subscription_history, SubscriptionHistoryInDB)
        assert (
            created_subscription_history.transaction_id
            == new_subscription.transaction_id
        )
        assert (
            created_subscription_history.user_telegram_id
            == new_subscription.user_telegram_id
        )
        assert created_subscription_history.amount == new_subscription.balance

        # Test creating a subscription history that has a wrong user id
        new_subscription_history.user_telegram_id = 59999
        invalid_subscription_history = (
            await subscription_history_repo.add_subscription_history(
                subscription_history_create=new_subscription_history
            )
        )
        assert invalid_subscription_history is None

    async def test_get_all_subscription_history_by_user_telegram_id(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription: SubscriptionCreate,
    ) -> None:
        """Test getting subscription history by user telegram id."""
        db, r_db = await db, await r_db
        subscription_history_repo = SubscriptionHistoryRepository(db, r_db)
        subscription_history = await subscription_history_repo.get_all_subscription_history_by_user_telegram_id(
            user_telegram_id=new_subscription.user_telegram_id
        )
        assert subscription_history is not None
        assert len(subscription_history) == 1
        assert (
            subscription_history[0].user_telegram_id
            == new_subscription.user_telegram_id
        )
        assert subscription_history[0].amount == new_subscription.balance

    async def test_get_all_subscription_history_by_subscription_id(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription_history: SubscriptionHistoryCreate,
        new_subscription: SubscriptionCreate,
    ) -> None:
        """Test getting subscription history by subscription id."""
        db, r_db = await db, await r_db
        subscription_history_repo = SubscriptionHistoryRepository(db, r_db)
        subscription = await SubscriptionRepository(db, r_db).upsert_new_subscription(
            new_subscription=new_subscription
        )
        subscription_history = (
            await subscription_history_repo.get_all_subscription_history_by_subscription_id(
                subscription_id=subscription.id
            )
        )
        assert subscription_history is not None
        assert len(subscription_history) == 1
        assert subscription_history[0].transaction_id == new_subscription.transaction_id
        assert (
            subscription_history[0].user_telegram_id
            == new_subscription.user_telegram_id
        )
        assert subscription_history[0].amount == new_subscription.balance

    async def test_get_all_subscription(
        self, client: AsyncClient, db: Database, r_db: Redis
    ) -> None:
        """Test getting all subscription history."""
        db, r_db = await db, await r_db
        subscription_history_repo = SubscriptionHistoryRepository(db, r_db)
        subscription_history = (
            await subscription_history_repo.get_all_subscription_history()
        )
        assert subscription_history is not None
        assert len(subscription_history) == 1
