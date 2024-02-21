"""Subscriptions repository test."""

import pytest
from databases import Database
from httpx import AsyncClient
from redis.asyncio import Redis

from src.db.repositories.subscriptions import SubscriptionRepository
from src.db.repositories.users import UserRepository
from src.models.subscriptions import SubscriptionCreate, SubscriptionInDB
from src.models.users import UserCreate

pytestmark = pytest.mark.asyncio


class TestSubscriptionsRepo:
    """Subscriptions repository test."""

    async def test_create_new_subscription(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_user: UserCreate,
        new_subscription: SubscriptionCreate,
        new_subscription_two: SubscriptionCreate,
    ) -> None:
        """Test creating a new subscription."""
        await UserRepository(db, r_db).add_new_user(new_user=new_user)
        subscription_repo = SubscriptionRepository(db, r_db)
        created_subscription = await subscription_repo.upsert_new_subscription(
            new_subscription=new_subscription
        )
        assert isinstance(created_subscription, SubscriptionInDB)
        assert (
            created_subscription.user_telegram_id == new_subscription.user_telegram_id
        )
        assert created_subscription.tier.tier_name == new_subscription.tier
        assert created_subscription.balance == new_subscription.balance

        # Test creating a subscription to top up
        duplicate_subscription = await subscription_repo.upsert_new_subscription(
            new_subscription=new_subscription_two
        )
        assert duplicate_subscription is not None
        assert (
            duplicate_subscription.user_telegram_id == new_subscription.user_telegram_id
        )

        assert (
            duplicate_subscription.balance
            == new_subscription.balance + new_subscription_two.balance
        )

        # Test creating a subscription for a user that doesn't exist.
        new_subscription.user_telegram_id = 0
        invalid_subscription = await subscription_repo.upsert_new_subscription(
            new_subscription=new_subscription
        )
        assert invalid_subscription is None

    async def test_get_all_subscriptions(
        self, client: AsyncClient, db: Database, r_db: Redis
    ) -> None:
        """Test retrieving all subscriptions."""
        subscription_repo = SubscriptionRepository(db, r_db)
        all_subscriptions = await subscription_repo.get_all_subscriptions()
        assert len(all_subscriptions) == 1
        assert all(
            isinstance(subscription, SubscriptionInDB)
            for subscription in all_subscriptions
        )

    async def test_get_subscription_by_user_telegram_id(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription: SubscriptionCreate,
        new_subscription_two: SubscriptionCreate,
    ) -> None:
        """Test retrieving subscription by user telegram id."""
        subscription_repo = SubscriptionRepository(db, r_db)
        subscription = await subscription_repo.get_subscription_by_user_telegram_id(
            user_telegram_id=new_subscription.user_telegram_id
        )
        assert isinstance(subscription, SubscriptionInDB)
        assert subscription.user_telegram_id == new_subscription.user_telegram_id
        assert subscription.tier == new_subscription_two.tier
        assert (
            subscription.balance
            == new_subscription.balance + new_subscription_two.balance
        )

    async def test_get_subscription_by_transaction_id(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription: SubscriptionCreate,
        new_subscription_two: SubscriptionCreate,
    ) -> None:
        """Test retrieving subscription by transaction id."""
        subscription_repo = SubscriptionRepository(db, r_db)
        subscription = await subscription_repo.get_subscription_by_transaction_id(
            transaction_id=new_subscription_two.transaction_id
        )
        assert isinstance(subscription, SubscriptionInDB)
        assert subscription.user_telegram_id == new_subscription_two.user_telegram_id
        assert subscription.tier == new_subscription_two.tier
        assert (
            subscription.balance
            == new_subscription_two.balance + new_subscription.balance
        )

    async def test_get_all_subscriptions_by_tier(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription_two: SubscriptionCreate,
    ) -> None:
        """Test retrieving all subscriptions by tier."""
        subscription_repo = SubscriptionRepository(db, r_db)
        all_subscriptions = await subscription_repo.get_all_subscriptions_by_tier(
            tier=new_subscription_two.tier.tier_name
        )
        assert len(all_subscriptions) == 1
        assert all(
            isinstance(subscription, SubscriptionInDB)
            for subscription in all_subscriptions
        )

    async def test_get_all_active_subscriptions(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
    ) -> None:
        """Test retrieving all active subscriptions."""
        subscription_repo = SubscriptionRepository(db, r_db)
        all_subscriptions = await subscription_repo.get_all_active_subscriptions()
        assert len(all_subscriptions) == 1
        assert all(
            isinstance(subscription, SubscriptionInDB)
            for subscription in all_subscriptions
        )

    async def test_update_subscription_balance(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription: SubscriptionCreate,
        new_subscription_two: SubscriptionCreate,
    ) -> None:
        """Test updating subscription balance."""
        total_balance = new_subscription.balance + new_subscription_two.balance
        subscription_repo = SubscriptionRepository(db, r_db)
        updated_subscription = await subscription_repo.update_subscription_balance(
            user_telegram_id=new_subscription.user_telegram_id,
            new_balance=total_balance - 10,
        )
        assert updated_subscription is not None
        assert updated_subscription.balance == total_balance - 10
        # Invalid user
        invalid_subscription = await subscription_repo.update_subscription_balance(
            user_telegram_id=0,
            new_balance=total_balance * 2,
        )
        assert invalid_subscription is None
        # Subscription balance can't be negative.
        with pytest.raises(ValueError) as value_error:
            await subscription_repo.update_subscription_balance(
                user_telegram_id=new_subscription.user_telegram_id,
                new_balance=total_balance * -2,
            )
            assert "Deducted value should not be less than 0" in str(value_error.value)

        # Amount deducted should never be greater than current subscription.
        with pytest.raises(ValueError) as value_error:
            await subscription_repo.update_subscription_balance(
                user_telegram_id=new_subscription.user_telegram_id,
                new_balance=updated_subscription.balance * 3,
            )
            assert (
                "Value being deducted should not be greater than current balance."
                in str(value_error.value)
            )

    async def test_delete_subscription(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_subscription: SubscriptionCreate,
    ) -> None:
        """Test deleting a subscription."""
        subscription_repo = SubscriptionRepository(db, r_db)
        # deleting with a wrong telegram id.
        await subscription_repo.delete_subscription_by_user_telegram_id(
            user_telegram_id=0
        )
        subscriptions = await subscription_repo.get_all_subscriptions()
        assert len(subscriptions) == 1

        deleted_subscription = (
            await subscription_repo.delete_subscription_by_user_telegram_id(
                user_telegram_id=new_subscription.user_telegram_id
            )
        )
        assert isinstance(deleted_subscription, int)
        subscription = await subscription_repo.get_subscription_by_user_telegram_id(
            user_telegram_id=new_subscription.user_telegram_id
        )
        assert subscription is None
        subscriptions = await subscription_repo.get_all_subscriptions()
        assert len(subscriptions) == 0
