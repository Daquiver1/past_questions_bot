"""Test route for subscription history."""

from fastapi import FastAPI
from httpx import AsyncClient

from src.models.users import UserPublic


class TestSubscriptionHistoryRoute:
    """Test cases for subscription history route."""

    async def test_get_all_subscription_history(
        self, app: FastAPI, client: AsyncClient, admin_fixture_helper: UserPublic
    ) -> None:
        """Test getting all subscription history."""
        response = await client.get(
            app.url_path_for("subscription_history:get-all"),
            headers={"X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id)},
        )
        assert response.status_code == 200
        subscription_history_data = response.json()
        assert len(subscription_history_data) == 0

    async def test_get_all_subscription_history_by_subscription_id(
        self, app: FastAPI, client: AsyncClient, admin_fixture_helper: UserPublic
    ) -> None:
        """Test getting subscription history by subscription id."""
        response = await client.get(
            app.url_path_for(
                "subscription_history:get-all-by-subscription-id", subscription_id=1
            ),
            headers={"X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id)},
        )
        assert response.status_code == 200
        subscription_history_data = response.json()
        assert len(subscription_history_data) == 0

    async def test_get_all_subscription_history_by_telegram_id(
        self, app: FastAPI, client: AsyncClient, admin_fixture_helper: UserPublic
    ) -> None:
        """Test getting subscription history by telegram id."""
        response = await client.get(
            app.url_path_for(
                "subscription_history:get-all-by-telegram-id",
            ),
            headers={
                "X-Admin-Telegram-ID": str(admin_fixture_helper.telegram_id),
                "X-Telegram-ID": str(admin_fixture_helper.telegram_id),
            },
        )
        assert response.status_code == 200
        subscription_history_data = response.json()
        assert len(subscription_history_data) == 0
