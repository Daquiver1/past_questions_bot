"""Db repo for Past Questions."""

from typing import Optional, Union

from databases import Database
from redis.asyncio import Redis

from src.db.repositories.base import BaseRepository
from src.models.past_question_filter_enum import PastQuestionFilter
from src.models.past_questions import PastQuestionCreate, PastQuestionInDB
from src.utils.generate_pasco_unique_code import generate_pasco_unique_code

ADD_PAST_QUESTION_QUERY = """
    INSERT INTO past_questions (course_code, course_name, course_title,lecturer_name,hash_key,  past_question_url, semester, year, updated_at)
    VALUES (:course_code, :course_name, :course_title, :lecturer_name,:hash_key, :past_question_url, :semester, :year, :updated_at)
    RETURNING id, course_code, course_name, course_title, lecturer_name, hash_key, past_question_url, semester, year, created_At, updated_At;
"""

GET_PAST_QUESTION_BY_PAST_QUESTION_ID_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name, hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE id = :past_question_id;
    """

GET_PAST_QUESTION_BY_COURSE_CODE_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE course_code = :course_code;
    """

GET_PAST_QUESTION_BY_COURSE_NAME_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE course_name = :course_name;
    """

GET_PAST_QUESTION_BY_COURSE_TITLE_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE course_title = :course_title;
    """

GET_PAST_QUESTION_BY_LECTURER_NAME_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE lecturer_name = :lecturer_name;
    """

GET_PAST_QUESTION_BY_SEMESTER_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE semester = :semester;
    """

GET_PAST_QUESTION_BY_YEAR_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE year = :year;
    """

GET_PAST_QUESTION_BY_HASH_KEY_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions
    WHERE hash_key = :hash_key;"""

GET_ALL_PAST_QUESTIONS_QUERY = """
    SELECT id, course_code, course_name, course_title, lecturer_name,hash_key, past_question_url, semester, year, created_at, updated_at
    FROM past_questions;
    """

DELETE_PAST_QUESTION_BY_PAST_QUESTION_ID_QUERY = """
    DELETE FROM past_questions
    WHERE id = :past_question_id
    RETURNING id;
"""


class PastQuestionRepository(BaseRepository):
    """All db actions associated with the past question resource."""

    def __init__(self, db: Database, r_db: Redis) -> None:
        """Initialize db"""
        super().__init__(db, r_db)

    async def add_new_past_question(
        self, *, new_past_question: PastQuestionCreate
    ) -> Optional[PastQuestionInDB]:
        """Create new past question data."""
        hash_key = generate_pasco_unique_code(new_past_question)
        if await self.get_all_past_questions_by_filter(
            PastQuestionFilter.HASH_KEY, hash_key
        ):
            return None

        updated_past_question = new_past_question.model_dump()
        updated_past_question["hash_key"] = hash_key
        past_question = await self.db.fetch_one(
            query=ADD_PAST_QUESTION_QUERY,
            values=updated_past_question,
        )
        if past_question:
            return PastQuestionInDB(**past_question)
        return None

    async def get_past_question(
        self, filter_by: PastQuestionFilter, filter_value: Union[int, str]
    ) -> Optional[PastQuestionInDB]:
        """Get past question data based on different filters."""
        query_mapping = {
            "past_question_id": GET_PAST_QUESTION_BY_PAST_QUESTION_ID_QUERY,
            "course_code": GET_PAST_QUESTION_BY_COURSE_CODE_QUERY,
            "course_name": GET_PAST_QUESTION_BY_COURSE_NAME_QUERY,
            "course_title": GET_PAST_QUESTION_BY_COURSE_TITLE_QUERY,
            "lecturer_name": GET_PAST_QUESTION_BY_LECTURER_NAME_QUERY,
            "semester": GET_PAST_QUESTION_BY_SEMESTER_QUERY,
            "hash_key": GET_PAST_QUESTION_BY_HASH_KEY_QUERY,
            "year": GET_PAST_QUESTION_BY_YEAR_QUERY,
        }
        query = query_mapping.get(filter_by.value)
        print(filter_by, filter_value, query)

        if not query:
            print("invalid filter")
            return None

        past_question = await self.db.fetch_one(
            query=query,
            values={filter_by.value: filter_value},
        )
        if past_question:
            return PastQuestionInDB(**past_question)
        return None

    async def get_all_past_questions(self) -> list[PastQuestionInDB]:
        """Get all past questions data."""
        past_questions = await self.db.fetch_all(query=GET_ALL_PAST_QUESTIONS_QUERY)
        return [PastQuestionInDB(**past_question) for past_question in past_questions]

    async def get_all_past_questions_by_filter(
        self, filter_by: PastQuestionFilter, filter_value: Union[int, str]
    ) -> list[PastQuestionInDB]:
        """Get past question data based on different filters.

        Parameters:
        - filter_by: A string representing the filter type (e.g., "past_question_id", "course_code").
        - filter_value: The value to filter by (can be int or str, depending on the filter).
        """
        query_mapping = {
            "past_question_id": GET_PAST_QUESTION_BY_PAST_QUESTION_ID_QUERY,
            "course_code": GET_PAST_QUESTION_BY_COURSE_CODE_QUERY,
            "course_name": GET_PAST_QUESTION_BY_COURSE_NAME_QUERY,
            "course_title": GET_PAST_QUESTION_BY_COURSE_TITLE_QUERY,
            "lecturer_name": GET_PAST_QUESTION_BY_LECTURER_NAME_QUERY,
            "hash_key": GET_PAST_QUESTION_BY_HASH_KEY_QUERY,
            "semester": GET_PAST_QUESTION_BY_SEMESTER_QUERY,
            "year": GET_PAST_QUESTION_BY_YEAR_QUERY,
        }

        query = query_mapping.get(filter_by.value)
        if not query:
            print("invalid filter")
            return []

        past_questions = await self.db.fetch_all(
            query=query,
            values={filter_by.value: filter_value},
        )
        return [PastQuestionInDB(**past_question) for past_question in past_questions]

    async def delete_past_question(self, *, past_question_id: int) -> int:
        """Delete past question data by past_question_id."""
        return await self.db.execute(
            query=DELETE_PAST_QUESTION_BY_PAST_QUESTION_ID_QUERY,
            values={"past_question_id": past_question_id},
        )
