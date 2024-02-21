"""DB repo for downloads."""

from typing import Optional

from databases import Database
from redis.asyncio import Redis

from src.db.repositories.base import BaseRepository
from src.db.repositories.past_questions import PastQuestionRepository
from src.db.repositories.users import UserRepository
from src.models.downloads import DownloadCreate, DownloadInDB
from src.models.past_question_filter_enum import PastQuestionFilter

ADD_DOWNLOAD_QUERY = """
    INSERT INTO downloads (user_telegram_id, past_question_id, updated_at)
    VALUES (:user_telegram_id, :past_question_id, :updated_at)
    RETURNING id, user_telegram_id, past_question_id, created_At, updated_At;
"""

GET_DOWNLOAD_BY_DOWNLOAD_ID_QUERY = """
    SELECT id, user_telegram_id, past_question_id, created_at, updated_at
    FROM downloads
    WHERE id = :id;
    """

GET_DOWNLOAD_BY_TELEGRAM_ID_QUERY = """
    SELECT id, user_telegram_id, past_question_id, created_at, updated_at
    FROM downloads
    WHERE user_telegram_id = :user_telegram_id;
    """

GET_DOWNLOAD_BY_PAST_QUESTION_ID_QUERY = """
    SELECT id, user_telegram_id, past_question_id, created_at, updated_at
    FROM downloads
    WHERE past_question_id = :past_question_id;
    """

GET_ALL_DOWNLOADS_QUERY = """
    SELECT id, user_telegram_id, past_question_id, created_at, updated_at
    FROM downloads;
    """

DELETE_DOWNLOAD_BY_DOWNLOAD_ID_QUERY = """
    DELETE FROM downloads
    WHERE id = :id
    RETURNING id;
"""


class DownloadRepository(BaseRepository):
    """All db actions associated with the downloads resource."""

    def __init__(self, db: Database, r_db: Redis) -> None:
        """Initialize db"""
        super().__init__(db, r_db)
        self.user_repo = UserRepository(db, r_db)
        self.past_questions_repo = PastQuestionRepository(db, r_db)

    async def add_new_download(
        self, *, new_download: DownloadCreate
    ) -> Optional[DownloadInDB]:
        """Create new downloads data."""
        if not await self.user_repo.get_user_details(
            telegram_id=new_download.user_telegram_id
        ):
            return None
        if not await self.past_questions_repo.get_past_question(
            filter_by=PastQuestionFilter.PAST_QUESTION_ID,
            filter_value=new_download.past_question_id,
        ):
            return None
        download = await self.db.fetch_one(
            query=ADD_DOWNLOAD_QUERY,
            values=new_download.model_dump(),
        )
        if download:
            return DownloadInDB(**download)
        return None

    async def get_all_user_downloads(self, telegram_id: int) -> list[DownloadInDB]:
        """Get user downloads data"""
        downloads = await self.db.fetch_all(
            query=GET_DOWNLOAD_BY_TELEGRAM_ID_QUERY,
            values={"user_telegram_id": telegram_id},
        )
        return [DownloadInDB(**download) for download in downloads]

    async def get_all_past_question_downloads(
        self, past_question_id: int
    ) -> list[DownloadInDB]:
        """Get past question downloads data"""
        downloads = await self.db.fetch_all(
            query=GET_DOWNLOAD_BY_PAST_QUESTION_ID_QUERY,
            values={"past_question_id": past_question_id},
        )
        return [DownloadInDB(**download) for download in downloads]

    async def get_all_downloads(self) -> list[DownloadInDB]:
        """Get all downloads data"""
        downloads = await self.db.fetch_all(
            query=GET_ALL_DOWNLOADS_QUERY,
        )
        return [DownloadInDB(**download) for download in downloads]

    async def delete_download(self, *, id: int) -> str:
        """Delete downloads data"""
        return await self.db.execute(
            query=DELETE_DOWNLOAD_BY_DOWNLOAD_ID_QUERY,
            values={"id": id},
        )
