"""Database fixtures for testing user."""

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


ROOT_DIR = Path(__file__).parent.parent.parent

sys.path.append(str(ROOT_DIR))
from src.models.past_questions import PastQuestionCreate, PastQuestionInDB
from src.models.users import UserCreate
from src.utils.generate_pasco_unique_code import generate_pasco_unique_code


@pytest.fixture(scope="session")
def apply_migrations() -> Generator[None, None, None]:
    """Handle db migrations."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    print("Applying migrations...")
    alembic.command.upgrade(config, "head")  # type: ignore
    yield
    print("Rolling back migrations...")
    alembic.command.downgrade(config, "base")  # type: ignore


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    """Handle db migrations."""
    from src.api.main import get_application

    return get_application()


@pytest.fixture
async def db(app: FastAPI) -> Database:
    """Sqlite db object."""
    await app.router.startup()
    return app.state._db


@pytest.fixture
async def r_db(app: FastAPI) -> Database:
    """Redis database object."""
    await app.router.startup()
    return app.state._redis


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    """Make request for test."""
    # TODO: Fix issue with lifespan not executing startup and shutdown
    async with LifespanManager(app, startup_timeout=20):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture
def new_user() -> UserCreate:
    """Return a UserCreate instance."""
    return UserCreate(
        username="testuser",
        first_name="test",
        telegram_id=12345678,
        last_name="test",
    )


@pytest.fixture
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


@pytest.fixture
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
