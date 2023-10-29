import warnings

import alembic
import pytest
from alembic.config import Config
from databases import Database

from models.past_question import PastQuestionCreate


# apply migration at beginning and end of testing session
@pytest.fixture(scope="function")
def apply_migrations():
    """Handle db migrations."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    config = Config("alembic.ini")
    print("Applying migrations...")
    alembic.command.upgrade(config, "head")  # type: ignore
    yield
    print("Rolling back migrations...")
    alembic.command.downgrade(config, "base")  # type: ignore


@pytest.fixture(scope="function")
async def db(apply_migrations) -> Database:
    print("Setting up database...")
    database = Database("sqlite:///app.db")
    await database.connect()
    print("Database connected", database)
    return database


@pytest.fixture
def new_past_question() -> PastQuestionCreate:
    return PastQuestionCreate(
        course_code="DCIT 104",
        course_name="Microsoft office and productivity tools.",
        lecturer="Michael Soli",
        past_question_url="http://example.com",
        semester="First",
        year="2022",
    )
