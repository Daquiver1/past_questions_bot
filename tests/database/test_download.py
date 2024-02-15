"""Download repository test."""

import pytest
from databases import Database
from httpx import AsyncClient
from redis.asyncio import Redis

from src.db.repositories.downloads import DownloadRepository
from src.db.repositories.past_questions import PastQuestionRepository
from src.db.repositories.users import UserRepository
from src.models.downloads import DownloadCreate, DownloadInDB
from src.models.past_questions import PastQuestionCreate
from src.models.users import UserCreate

pytestmark = pytest.mark.asyncio


class TestDownloadRepo:
    """Download repository test."""

    async def test_create_new_download(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_user: UserCreate,
        new_past_question: PastQuestionCreate,
        new_download: DownloadCreate,
    ) -> None:
        """Test creating a new download."""
        db, r_db = await db, await r_db
        download_repo = DownloadRepository(db, r_db)
        await UserRepository(db, r_db).add_new_user(new_user=new_user)
        await PastQuestionRepository(db, r_db).add_new_past_question(
            new_past_question=new_past_question
        )
        created_download = await download_repo.add_new_download(
            new_download=new_download
        )
        assert isinstance(created_download, DownloadInDB)
        assert created_download.user_telegram_id == new_download.user_telegram_id
        assert created_download.past_question_id == new_download.past_question_id

        # Test creating a download with invalid user
        invalid_user_download = new_download.model_copy(update={"user_telegram_id": 0})
        invalid_user_download = await download_repo.add_new_download(
            new_download=invalid_user_download
        )
        assert invalid_user_download is None

        # Test creating a download with invalid past question
        invalid_past_question_download = new_download.model_copy(update={"past_question_id": 0})
        invalid_past_question_download = await download_repo.add_new_download(
            new_download=invalid_past_question_download
        )
        assert invalid_past_question_download is None

    async def test_get_all_user_downloads(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_download: DownloadCreate,
    ) -> None:
        """Test getting all user downloads."""
        db, r_db = await db, await r_db
        download_repo = DownloadRepository(db, r_db)
        user_downloads = await download_repo.get_all_user_downloads(
            telegram_id=new_download.user_telegram_id
        )
        assert len(user_downloads) == 1
        assert user_downloads[0].user_telegram_id == new_download.user_telegram_id

    async def test_get_all_past_question_downloads(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_download: DownloadCreate,
    ) -> None:
        """Test getting all past question downloads."""
        db, r_db = await db, await r_db
        download_repo = DownloadRepository(db, r_db)
        past_question_downloads = await download_repo.get_all_past_question_downloads(
            past_question_id=new_download.past_question_id
        )
        assert len(past_question_downloads) == 1
        assert (
            past_question_downloads[0].past_question_id == new_download.past_question_id
        )

    async def test_get_all_downloads(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_download: DownloadCreate,
    ) -> None:
        """Test getting all downloads."""
        db, r_db = await db, await r_db
        download_repo = DownloadRepository(db, r_db)
        all_downloads = await download_repo.get_all_downloads()
        assert len(all_downloads) == 1
        assert all_downloads[0].user_telegram_id == new_download.user_telegram_id
        assert all_downloads[0].past_question_id == new_download.past_question_id

    async def test_delete_download_by_id(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
    ) -> None:
        """Test deleting a download."""
        db, r_db = await db, await r_db
        download_repo = DownloadRepository(db, r_db)
        await download_repo.delete_download(
            id=1,
        )
        downloads = await download_repo.get_all_downloads()
        assert len(downloads) == 0
