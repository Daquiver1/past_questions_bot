"""Test route for  subscriptions"""

from fastapi import FastAPI
from httpx import AsyncClient

from src.models.users import UserPublic


class TestSubscriptionRoute:
    """Test cases for subscription route."""

    async def test_create_new_subscription(
        self,
        app: FastAPI,
        client: AsyncClient,
        valid_subscription_create: dict[str, str],
        user_fixture_helper1: UserPublic,
    ) -> None:
        """Test creating a new subscription."""
        # Creating a subscription
        response = await client.post(
            app.url_path_for("subscriptions:create-subscription"),
            json=valid_subscription_create,
            headers={"X-Telegram-ID": str(user_fixture_helper1.telegram_id)},
        )
        assert response.status_code == 201
        subscription_data = response.json()
        assert (
            subscription_data["user_telegram_id"]
            == valid_subscription_create["user_telegram_id"]
        )

        # Topping up the subscription
        valid_subscription_create["transaction_id"] = "1234567890"
        response = await client.post(
            app.url_path_for("subscriptions:create-subscription"),
            json=valid_subscription_create,
            headers={"X-Telegram-ID": str(user_fixture_helper1.telegram_id)},
        )

        assert response.status_code == 201
        assert response.json()["balance"] == 10

    async def test_get_subscription_details(
        self,
        app: FastAPI,
        client: AsyncClient,
        user_fixture_helper1: UserPublic,
        user_fixture_helper2: UserPublic,
    ) -> None:
        """Test getting subscription details."""
        # User has a subscription
        response = await client.get(
            app.url_path_for("subscriptions:get-subscription-by-telegram-id"),
            headers={"X-Telegram-ID": str(user_fixture_helper1.telegram_id)},
        )
        assert response.status_code == 200
        subscription_data = response.json()
        assert subscription_data["user_telegram_id"] == user_fixture_helper1.telegram_id

        # User doesn't have  a subscription
        response = await client.get(
            app.url_path_for("subscriptions:get-subscription-by-telegram-id"),
            headers={"X-Telegram-ID": str(user_fixture_helper2.telegram_id)},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Subscription not found"

    async def test_get_all_active_subscriptions(
        self, app: FastAPI, client: AsyncClient, admin_fixture_helper: UserPublic
    ) -> None:
        """Test getting all active subscriptions."""
        response = await client.get(
            app.url_path_for("subscriptions:get-all-active-subscriptions"),
            headers={"X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id)},
        )
        assert response.status_code == 200
        subscriptions_data = response.json()
        assert len(subscriptions_data) == 1

    async def test_get_all_subscriptions(
        self, app: FastAPI, client: AsyncClient, admin_fixture_helper: UserPublic
    ) -> None:
        """Test getting all subscriptions."""
        response = await client.get(
            app.url_path_for("subscriptions:get-all-subscriptions"),
            headers={"X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id)},
        )
        assert response.status_code == 200
        subscriptions_data = response.json()
        assert len(subscriptions_data) == 1

    async def test_update_subscription_balance(
        self,
        app: FastAPI,
        client: AsyncClient,
        user_fixture_helper1: UserPublic,
        user_fixture_helper2: UserPublic,
    ) -> None:
        """Test updating subscription balance."""
        # User with subscription
        response = await client.patch(
            app.url_path_for("subscriptions:update-subscription-balance", balance=8),
            headers={"X-Telegram-ID": str(user_fixture_helper1.telegram_id)},
        )
        assert response.status_code == 200
        subscription_data = response.json()
        assert subscription_data["balance"] == 8

        # User without subscription
        response = await client.patch(
            app.url_path_for("subscriptions:update-subscription-balance", balance=2),
            headers={"X-Telegram-ID": str(user_fixture_helper2.telegram_id)},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Subscription not found"

    async def test_delete_subscription(
        self,
        app: FastAPI,
        client: AsyncClient,
        admin_fixture_helper: UserPublic,
        user_fixture_helper1: UserPublic,
        user_fixture_helper2: UserPublic,
    ) -> None:
        """Test deleting a subscription."""
        response = await client.delete(
            app.url_path_for("subscriptions:delete-subscription"),
            headers={
                "X-Telegram-ID": str(user_fixture_helper1.telegram_id),
                "X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id),
            },
        )
        assert response.status_code == 200

        # User without subscription
        response = await client.delete(
            app.url_path_for("subscriptions:delete-subscription"),
            headers={
                "X-Telegram-ID": str(user_fixture_helper2.telegram_id),
                "X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id),
            },
        )
        assert response.status_code == 200
