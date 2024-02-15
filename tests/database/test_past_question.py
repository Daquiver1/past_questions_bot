
"""Past questions repository tests."""

import pytest
from databases import Database
from httpx import AsyncClient
from redis.asyncio import Redis

from src.models.past_question_filter_enum import PastQuestionFilter
from src.db.repositories.past_questions import PastQuestionRepository
from src.models.past_questions import PastQuestionCreate, PastQuestionInDB

pytestmark = pytest.mark.asyncio


class TestPastQuestionRepo:
    """Past questions repository tests."""

    async def test_create_new_past_question(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        new_past_question: PastQuestionCreate,
        past_question_in_db: PastQuestionInDB,
    ) -> None:
        """Test creating a new past question."""
        db, r_db = await db, await r_db
        past_question_repo = PastQuestionRepository(db, r_db)
        created_past_question = await past_question_repo.add_new_past_question(
            new_past_question=new_past_question
        )
        assert isinstance(created_past_question, PastQuestionInDB)
        print(created_past_question)
        assert created_past_question.hash_key == past_question_in_db.hash_key

        # Test creating a past question that already exists
        duplicate_past_question = await past_question_repo.add_new_past_question(
            new_past_question=new_past_question
        )
        assert duplicate_past_question is None

    async def test_get_all_past_questions(
        self, client: AsyncClient, db: Database, r_db: Redis
    ) -> None:
        """Test retrieving all past questions."""
        db, r_db = await db, await r_db
        past_question_repo = PastQuestionRepository(db, r_db)
        all_past_questions = await past_question_repo.get_all_past_questions()
        assert len(all_past_questions) == 1
        assert all(
            isinstance(past_question, PastQuestionInDB)
            for past_question in all_past_questions
        )

    @pytest.mark.parametrize(
        "filter_by,filter_value",
        [
            (PastQuestionFilter.PAST_QUESTION_ID, 1),
            (PastQuestionFilter.COURSE_CODE, "104"),
            (PastQuestionFilter.COURSE_NAME, "test"),
            (PastQuestionFilter.COURSE_TITLE, "test 104"),
            (PastQuestionFilter.LECTURER_NAME, "Test Test"),
            (
                PastQuestionFilter.HASH_KEY,
                "a8b9db5db2ff5e37ec593536573d6d61c7baa00713f3642b2515fa839bac45dd",
            ),
            (PastQuestionFilter.SEMESTER, "First"),
            (PastQuestionFilter.YEAR, "2022"),
        ],
    )
    async def test_get_past_question_details(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        past_question_in_db: PastQuestionInDB,
        filter_by: PastQuestionFilter,
        filter_value: str,
    ) -> None:
        """Test retrieving past question details."""
        db, r_db = await db, await r_db
        past_question_repo = PastQuestionRepository(db, r_db)
        past_question = await past_question_repo.get_past_question(
            filter_by=filter_by, filter_value=filter_value
        )
        assert isinstance(past_question, PastQuestionInDB)
        assert past_question.id == past_question_in_db.id
        assert past_question.hash_key == past_question_in_db.hash_key
        past_question = await past_question_repo.get_past_question(
            filter_by=PastQuestionFilter.HASH_KEY, filter_value="invalid_value"
        )
        assert past_question is None

    @pytest.mark.parametrize(
        "filter_by,filter_value",
        [
            (PastQuestionFilter.PAST_QUESTION_ID, 1),
            (PastQuestionFilter.COURSE_CODE, "104"),
            (PastQuestionFilter.COURSE_NAME, "test"),
            (PastQuestionFilter.COURSE_TITLE, "test 104"),
            (PastQuestionFilter.LECTURER_NAME, "Test Test"),
            (
                PastQuestionFilter.HASH_KEY,
                "a8b9db5db2ff5e37ec593536573d6d61c7baa00713f3642b2515fa839bac45dd",
            ),
            (PastQuestionFilter.SEMESTER, "First"),
            (PastQuestionFilter.YEAR, "2022"),
        ],
    )
    async def test_get_all_past_question_details(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        filter_by: PastQuestionFilter,
        filter_value: str,
    ) -> None:
        """Test retrieving past question details."""
        db, r_db = await db, await r_db
        past_question_repo = PastQuestionRepository(db, r_db)
        past_questions = await past_question_repo.get_all_past_questions_by_filter(
            filter_by=filter_by, filter_value=filter_value
        )
        assert isinstance(past_questions, list)
        assert len(past_questions) == 1
        past_questions = await past_question_repo.get_all_past_questions_by_filter(
            filter_by=PastQuestionFilter.HASH_KEY, filter_value="invalid_value"
        )
        assert len(past_questions) == 0

    async def test_delete_past_question(
        self,
        client: AsyncClient,
        db: Database,
        r_db: Redis,
        past_question_in_db: PastQuestionInDB,
    ) -> None:
        """Test deleting a past question."""
        db, r_db = await db, await r_db
        past_question_repo = PastQuestionRepository(db, r_db)
        past_question_delete = await past_question_repo.delete_past_question(
            past_question_id=past_question_in_db.id
        )
        assert isinstance(past_question_delete, int)
        past_question = await past_question_repo.get_all_past_questions()
        assert len(past_question) == 0
