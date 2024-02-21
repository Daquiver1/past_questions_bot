"""FastAPI fixtures for testing."""

import asyncio
import sys
import warnings
from pathlib import Path
from typing import AsyncGenerator, Callable, Generator, Union

import alembic
import pytest
from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import Redis

ROOT_DIR = Path(__file__).parent.parent.parent

sys.path.append(str(ROOT_DIR))
from src.core.config import ADMIN_TELEGRAM_ID
from src.db.repositories.users import UserRepository
from src.models.users import UserCreate, UserPublic


@pytest.fixture(scope="class")
def apply_migrations() -> Generator[None, None, None]:
    """Handle db migrations."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    print("Applying migrations...")
    alembic.command.upgrade(config, "head")  # type: ignore
    yield
    print("Rolling back migrations...")
    alembic.command.downgrade(config, "base")  # type: ignore


@pytest.fixture(scope="class")
def app(apply_migrations: None) -> FastAPI:
    """Handle db migrations."""
    # Third party imports
    from src.api.main import get_application

    return get_application()


@pytest.fixture(scope="class")
async def client(app: FastAPI) -> AsyncGenerator:
    """Make request for test."""
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as test_client:
            yield test_client


@pytest.fixture(scope="class")
def valid_user_create() -> dict[str, str]:
    """Return a valid user create."""
    return {
        "username": "test_user",
        "first_name": "test",
        "last_name": "user",
        "telegram_id": 123456789,
    }


@pytest.fixture(scope="class")
def valid_subscription_create() -> dict[str, str]:
    """Return a valid subscription create."""
    return {
        "user_telegram_id": 10829272,
        "tier": "Basic",
        "balance": "5",
        "transaction_id": "333333",
        "is_active": "true",
    }


@pytest.fixture(scope="class")
def valid_admin_create() -> dict[str, str]:
    """Return a valid admin create."""
    return {
        "username": "test_admin",
        "first_name": "test",
        "last_name": "admin",
        "telegram_id": ADMIN_TELEGRAM_ID,
    }


@pytest.fixture(scope="class")
def valid_past_question_create() -> Callable:
    """Fixture to return valid past question data."""

    def _data(
        file_content: bytes = b"dummy content",
    ) -> dict[str, Union[str, tuple[str, bytes, str]]]:
        """Return a valid past question create."""
        return {
            "file": ("filename.pdf", file_content, "application/pdf"),
            "course_name": (None, "Test"),
            "course_code": (None, "104"),
            "lecturer_name": (None, "Test Test"),
            "semester": (None, "First"),
            "year": (None, "2022"),
        }

    return _data


@pytest.fixture(scope="class")
def invalid_user_create() -> dict[str, str]:
    """Return an invalid user create."""
    return {
        "username": "test_user",
        "first_name": "test",
        "last_name": "user",
    }


# getting db
@pytest.fixture(scope="class")
def db(app: FastAPI) -> Database:
    """Postgres db object."""
    return app.state._db


@pytest.fixture(scope="class")
def r_db(app: FastAPI) -> Redis:
    """Redis database object."""
    return app.state._redis


@pytest.fixture(scope="class")
async def admin_fixture_helper(
    *, db: Database, r_db: Redis, valid_admin_create: dict[str, str]
) -> UserPublic:
    """Fixture helper to create user."""
    admin = UserCreate(**valid_admin_create)
    users_repo = UserRepository(db, r_db)
    existing_user = await users_repo.get_user_details(telegram_id=admin.telegram_id)
    if existing_user:
        return existing_user
    return await users_repo.add_new_user(new_user=admin)


@pytest.fixture(scope="class")
async def user_fixture_helper1(
    *, db: Database, r_db: Redis, test_user1: UserCreate
) -> UserPublic:
    """Fixture helper to create user."""
    users_repo = UserRepository(db, r_db)
    existing_user = await users_repo.get_user_details(
        telegram_id=test_user1.telegram_id
    )
    if existing_user:
        return existing_user
    return await users_repo.add_new_user(new_user=test_user1)


@pytest.fixture(scope="class")
async def user_fixture_helper2(
    *, db: Database, r_db: Redis, test_user2: UserCreate
) -> UserPublic:
    """Fixture helper to create user."""
    users_repo = UserRepository(db, r_db)
    existing_user = await users_repo.get_user_details(
        telegram_id=test_user2.telegram_id
    )
    if existing_user:
        return existing_user
    return await users_repo.add_new_user(new_user=test_user2)


@pytest.fixture(scope="class")
async def test_user1(db: Database, r_db: Redis) -> UserCreate:
    """Return a test user."""
    return UserCreate(
        username="test_user1",
        first_name="test",
        last_name="user1",
        telegram_id=10829272,
    )


@pytest.fixture(scope="class")
async def test_user2(db: Database, r_db: Redis) -> UserCreate:
    """Return a test user."""
    return UserCreate(
        username="test_user2",
        first_name="test2",
        last_name="user2",
        telegram_id=10829273,
    )
