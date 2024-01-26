"""DB repo for downloads."""

from databases import Database

from src.db.repositories.base import BaseRepository
from src.models.downloads import DownloadCreate, DownloadInDB

ADD_DOWNLOAD_QUERY = """
    INSERT INTO downloads (telegram_id, past_question_id)
    VALUES (:telegram_id, :past_question_id)
    RETURNING id, telegram_id, past_question_id, created_At, updated_At;
"""

GET_DOWNLOAD_BY_DOWNLOAD_ID_QUERY = """
    SELECT id, telegram_id, past_question_id, created_at, updated_at
    FROM downloads
    WHERE id = :id;
    """

GET_DOWNLOAD_BY_TELEGRAM_ID_QUERY = """
    SELECT id, telegram_id, past_question_id, created_at, updated_at
    FROM downloads
    WHERE telegram_id = :telegram_id;
    """

GET_DOWNLOAD_BY_PAST_QUESTION_ID_QUERY = """
    SELECT id, telegram_id, past_question_id, created_at, updated_at
    FROM downloads
    WHERE past_question_id = :past_question_id;
    """

GET_ALL_DOWNLOADS_QUERY = """
    SELECT id, telegram_id, past_question_id, created_at, updated_at
    FROM downloads;
    """

DELETE_DOWNLOAD_BY_DOWNLOAD_ID_QUERY = """
    DELETE FROM downloads
    WHERE id = :id
    RETURNING id;
"""


class DownloadRepository(BaseRepository):
    """All db actions associated with the downloads resource."""

    def __init__(self, db: Database) -> None:
        """Initialize db"""
        super().__init__(db)

    async def add_new_download(self, *, new_download: DownloadCreate) -> DownloadInDB:
        """Create new downloads data."""
        return await self.db.fetch_one(
            query=ADD_DOWNLOAD_QUERY,
            values=new_download.dict(),
        )

    async def get_all_user_downloads(self, telegram_id: str) -> list[DownloadInDB]:
        """Get user downloads data"""
        downloads = await self.db.fetch_all(
            query=GET_DOWNLOAD_BY_TELEGRAM_ID_QUERY,
            values={"telegram_id": telegram_id},
        )
        return downloads

    async def get_all_past_question_downloads(
        self, past_question_id: int
    ) -> list[DownloadInDB]:
        """Get past question downloads data"""
        downloads = await self.db.fetch_all(
            query=GET_DOWNLOAD_BY_PAST_QUESTION_ID_QUERY,
            values={"past_question_id": past_question_id},
        )
        return downloads

    async def delete_download(self, *, id: str) -> str:
        """Delete downloads data"""
        return await self.db.fetch_one(
            query=DELETE_DOWNLOAD_BY_DOWNLOAD_ID_QUERY,
            values={"id": id},
        )

    async def get_all_downloads(self) -> list[DownloadInDB]:
        """Get all downloads data"""
        downloads = await self.db.fetch_all(
            query=GET_ALL_DOWNLOADS_QUERY,
        )
        return downloads
