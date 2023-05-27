from typing import Coroutine

import pytest
from databases import Database

from db.repositories.user import UserRepository
from models.user import UserCreate, UserInDb

pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_user() -> UserCreate:
    return UserCreate(
        username="testuser",
        telegram_id="1234567890",
        is_subscribed=True,
        is_eligible=True,
        balance=100,
    )


async def test_create_new_user(
    db: Coroutine[None, None, Database], new_user: UserCreate
) -> None:
    # Test creating a new user
    database = await db  # db is received as a coroutine

    user_repo = UserRepository(database)
    created_user = await user_repo.create_new_user(new_user=new_user)
    assert isinstance(created_user, UserInDb)

    # Test creating a user that already exists
    duplicate_user = await user_repo.create_new_user(new_user=new_user)
    assert duplicate_user is None


async def test_get_user_by_telegram_id(
    db: Coroutine[None, None, Database], new_user: UserCreate
) -> None:
    # Test getting a user that doesn't exist
    database = await db
    user_repo = UserRepository(database)

    user = await user_repo.get_user_by_telegram_id(telegram_id="nonexistent")
    assert user is None

    # Test getting a user that does exist
    created_user = await user_repo.create_new_user(new_user=new_user)
    assert created_user is not None

    user = await user_repo.get_user_by_telegram_id(telegram_id=new_user.telegram_id)
    assert isinstance(user, UserInDb)
    assert user.telegram_id == created_user.telegram_id


async def test_update_user_is_subscribed(
    db: Coroutine[None, None, Database], new_user: UserCreate
) -> None:
    database = await db
    user_repo = UserRepository(database)
    # Test updating a user's subscription status
    created_user = await user_repo.create_new_user(new_user=new_user)
    assert created_user is not None

    updated_user = await user_repo.update_user_is_subscribed(
        value=False, telegram_id=new_user.telegram_id
    )
    assert isinstance(updated_user, UserInDb)
    assert created_user.is_subscribed != updated_user.is_subscribed
    assert updated_user.is_subscribed is False


async def test_update_user_is_eligible(db: Coroutine[None, None, Database], new_user):
    database = await db
    user_repo = UserRepository(database)
    # Test updating a user's eligibility status
    created_user = await user_repo.create_new_user(new_user=new_user)
    assert created_user is not None

    updated_user = await user_repo.update_user_is_eligible(
        value=False, telegram_id=new_user.telegram_id
    )
    assert isinstance(updated_user, UserInDb)
    assert created_user.is_eligible != updated_user.is_eligible
    assert updated_user.is_eligible is False


async def test_update_user_balance(
    db: Coroutine[None, None, Database], new_user: UserCreate
):
    database = await db
    user_repo = UserRepository(database)
    # Test updating a user's balance
    created_user = await user_repo.create_new_user(new_user=new_user)
    assert created_user is not None

    updated_user = await user_repo.update_user_balance(
        value=50, telegram_id=new_user.telegram_id
    )
    assert isinstance(updated_user, UserInDb)
    assert updated_user.balance == 50
