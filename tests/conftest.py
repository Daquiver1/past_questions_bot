import warnings

import alembic
import pytest
from alembic.config import Config
from databases import Database


# apply migration at beginning and end of testing session
@pytest.fixture(scope="function", autouse=True)
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
async def db() -> Database:
    print("Setting up database...")
    database = Database("sqlite:///app.db")
    await database.connect()
    print("Database connected", database)
    return database
