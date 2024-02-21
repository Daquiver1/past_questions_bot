"""User repository tests."""

import pytest
from databases import Database
from httpx import AsyncClient
from redis.asyncio import Redis

from src.db.repositories.users import UserRepository
from src.models.users import UserCreate, UserInDB

pytestmark = pytest.mark.asyncio


class TestUserRepo:
    """User repository tests."""

    async def test_create_new_user(
        self, client: AsyncClient, db: Database, r_db: Redis, new_user: UserCreate
    ) -> None:
        """Test creating a new user."""     
        user_repo = UserRepository(db, r_db)
        created_user = await user_repo.add_new_user(new_user=new_user)
        assert isinstance(created_user, UserInDB)

        # Test creating a user that already exists
        duplicate_user = await user_repo.add_new_user(new_user=new_user)
        assert duplicate_user is None

    async def test_get_all_users(
        self, client: AsyncClient, db: Database, r_db: Redis
    ) -> None:
        """Test retrieving all users."""    
        user_repo = UserRepository(db, r_db)
        all_users = await user_repo.get_all_users()
        assert len(all_users) == 1
        assert all(isinstance(user, UserInDB) for user in all_users)

    async def test_get_user_details(
        self, client: AsyncClient, db: Database, r_db: Redis, new_user: UserCreate
    ) -> None:
        """Test retrieving user details."""      
        user_repo = UserRepository(db, r_db)
        user = await user_repo.get_user_details(telegram_id=new_user.telegram_id)
        assert isinstance(user, UserInDB)
        assert user.telegram_id == new_user.telegram_id
        assert user.username == new_user.username
        user = await user_repo.get_user_details(telegram_id=987654321)
        assert user is None

    async def test_delete_user(
        self, client: AsyncClient, db: Database, r_db: Redis, new_user: UserCreate
    ) -> None:
        """Test deleting a user."""      
        user_repo = UserRepository(db, r_db)
        user_delete = await user_repo.delete_user(telegram_id=new_user.telegram_id)
        assert isinstance(user_delete, int)
        user = await user_repo.get_user_details(telegram_id=new_user.telegram_id)
        assert user is None
        user = await user_repo.get_all_users()
        assert len(user) == 0
