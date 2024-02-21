"""Test route for user."""

from fastapi import FastAPI
from httpx import AsyncClient


class TestUserRoute:
    """Test cases for user route."""

    async def test_create_new_user(
        self,
        app: FastAPI,
        client: AsyncClient,
        valid_user_create: dict[str, str],
        valid_admin_create: dict[str, str],
        invalid_user_create: dict[str, str],
    ) -> None:
        """Test creating a new user."""
        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json=valid_user_create,
        )
        assert response.status_code == 201
        user_data = response.json()
        assert user_data["telegram_id"] == valid_user_create["telegram_id"]

        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json=valid_admin_create,
        )
        assert response.status_code == 201
        user_data = response.json()
        assert user_data["telegram_id"] == valid_admin_create["telegram_id"]

        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json=valid_user_create,
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "User already created"

        response = await client.post(
            app.url_path_for("users:register-new-user"),
            json=invalid_user_create,
        )
        assert response.status_code == 422

    async def test_get_user_details(
        self,
        app: FastAPI,
        client: AsyncClient,
        valid_user_create: dict[str, str],
    ) -> None:
        """Test getting user details."""
        # Valid telegram id
        response = await client.get(
            app.url_path_for("users:get-user-details"),
            headers={"X-Telegram-ID": str(valid_user_create["telegram_id"])},
        )
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["telegram_id"] == valid_user_create["telegram_id"]

        # Invalid telegram  id type.
        response = await client.get(
            app.url_path_for("users:get-user-details"),
            headers={"X-Telegram-ID": "invalid"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid X-Telegram-ID header value"

        # Wrong telegram  ID.
        response = await client.get(
            app.url_path_for("users:get-user-details"),
            headers={"X-Telegram-ID": "10829272"},
        )
        assert response.status_code == 401
        assert (
            response.json()["detail"]
            == "User not found. Please register to use the service."
        )

        # No telegram ID header.
        response = await client.get(
            app.url_path_for("users:get-user-details"),
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "X-Telegram-ID header missing"

    async def test_get_all_users(
        self, app: FastAPI, client: AsyncClient, valid_admin_create: dict[str, str]
    ) -> None:
        """Test getting all users."""
        # Get  all users as admin.
        response = await client.get(
            app.url_path_for("users:get-all-users"),
            headers={"X-Admin-Telegram-ID": str(valid_admin_create["telegram_id"])},
        )
        assert response.status_code == 200
        users_data = response.json()
        assert len(users_data) == 2

        # Get all users with invalid admin header.
        response = await client.get(
            app.url_path_for("users:get-all-users"),
            headers={"X-Admin-Telegram-ID": "10829272"},
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"]
            == "Unauthorized. Only admin can access this endpoint."
        )

        # Get all users as client without admin header.
        response = await client.get(
            app.url_path_for("users:get-all-users"),
            headers={"X-Telegram-ID": "10829272"},
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Admin telegram id header missing"

    async def test_delete_user(
        self,
        app: FastAPI,
        client: AsyncClient,
        valid_user_create: dict[str, str],
        valid_admin_create: dict[str, str],
    ) -> None:
        """Test deleting a user."""
        # Delete user that does not exist.
        response = await client.delete(
            app.url_path_for("users:delete-user"),
            headers={
                "X-Telegram-ID": "108234843",
                "X-Admin-Telegram-ID": str(valid_admin_create["telegram_id"]),
            },
        )
        assert response.status_code == 401
        assert response.json() == {
            "detail": "User not found. Please register to use the service."
        }

        # Delete user with invalid telegram id.
        response = await client.delete(
            app.url_path_for("users:delete-user"),
            headers={
                "X-Telegram-ID": "invalid",
                "X-Admin-Telegram-ID": str(valid_admin_create["telegram_id"]),
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid X-Telegram-ID header value"}

        # Delete user with no telegram id header.
        response = await client.delete(
            app.url_path_for("users:delete-user"),
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Admin telegram id header missing"}

        # Delete user with wrong admin header
        response = await client.delete(
            app.url_path_for("users:delete-user"),
            headers={
                "X-Telegram-ID": str(valid_user_create["telegram_id"]),
                "X-Admin-Telegram-ID": "10829272",
            },
        )

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Unauthorized. Only admin can access this endpoint."
        }

        # Delete user.
        response = await client.delete(
            app.url_path_for("users:delete-user"),
            headers={
                "X-Telegram-ID": str(valid_user_create["telegram_id"]),
                "X-Admin-Telegram-ID": str(valid_admin_create["telegram_id"]),
            },
        )

        assert response.status_code == 200
