"""Database fixtures for testing."""

import sys
import warnings
from pathlib import Path
from typing import AsyncGenerator, Generator

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
from src.models.downloads import DownloadCreate
from src.models.past_questions import PastQuestionCreate, PastQuestionInDB
from src.models.subscriptions import SubscriptionCreate
from src.models.subscriptions_history import SubscriptionHistoryCreate
from src.models.users import UserCreate
from src.utils.generate_pasco_unique_code import generate_pasco_unique_code


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
    from src.api.main import get_application

    return get_application()


@pytest.fixture(scope="class")
def db(app: FastAPI) -> Database:
    """Sqlite db object."""
    return app.state._db


@pytest.fixture(scope="class")
def r_db(app: FastAPI) -> Redis:
    """Redis database object."""
    return app.state._redis


@pytest.fixture(scope="class")
async def client(app: FastAPI) -> AsyncGenerator:
    """Make request for test."""
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture(scope="class")
def new_user() -> UserCreate:
    """Return a UserCreate instance."""
    return UserCreate(
        username="testuser",
        first_name="test",
        telegram_id=12345678,
        last_name="test",
    )


@pytest.fixture(scope="class")
def new_past_question() -> PastQuestionCreate:
    """Return a PastQuestionCreate instance."""
    return PastQuestionCreate(
        course_code="104",
        course_name="Test",
        course_title="Test 104",
        lecturer_name="Test Test",
        past_question_url="http://example.com",
        semester="First",
        year="2022",
    )


@pytest.fixture(scope="class")
def past_question_in_db(new_past_question: PastQuestionCreate) -> PastQuestionInDB:
    """Return a PastQuestionInDB instance."""
    return PastQuestionInDB(
        id=1,
        course_code="104",
        course_name="Test",
        course_title="Test 104",
        hash_key=generate_pasco_unique_code(new_past_question),
        lecturer_name="Test Test",
        past_question_url="http://example.com",
        semester="First",
        year="2022",
        created_at="2022-01-01 00:00:00",
        updated_at="2022-01-01 00:00:00",
    )


@pytest.fixture(scope="class")
def new_subscription() -> SubscriptionCreate:
    """Return a SubscriptionCreate instance."""
    return SubscriptionCreate(
        user_telegram_id=12345678,
        transaction_id="10829272",
        tier="Basic",
        balance=5,
    )


@pytest.fixture(scope="class")
def new_subscription_two() -> SubscriptionCreate:
    """Return a SubscriptionCreate instance."""
    return SubscriptionCreate(
        user_telegram_id=12345678,
        transaction_id="103839373",
        tier="Premium",
        balance=35,
    )


@pytest.fixture(scope="class")
def new_subscription_history() -> SubscriptionHistoryCreate:
    """Return a SubscriptionCreateHistory instance."""
    return SubscriptionHistoryCreate(
        user_telegram_id=12345678,
        transaction_id="10829272",
        tier="Basic",
        amount=5,
        subscription_id=0,
    )


@pytest.fixture(scope="class")
def new_download() -> DownloadCreate:
    """Return a DownloadCreate instance."""
    return DownloadCreate(
        user_telegram_id=12345678,
        past_question_id=1,
    )
