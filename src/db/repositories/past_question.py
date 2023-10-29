"""SqlLite past_question repository."""
from typing import List, Union

from db.repositories.base import BaseRepository
from models.past_question import PastQuestionCreate, PastQuestionInDb
from utils.uuid import generate_n_digit_uuid

CREATE_NEW_PAST_QUESTION_QUERY = """
    INSERT INTO past_questions (course_code, course_name, lecturer, past_question_url, semester, year, category_id, uuid)
    VALUES (:course_code, :course_name, :lecturer, :past_question_url, :semester, :year, :category_id, :uuid)
"""

DELETE_PAST_QUESTION_BY_ID_QUERY = """
    DELETE FROM past_questions
    WHERE id = :id;
"""

GET_PAST_QUESTION_BY_ID_QUERY = """
    SELECT *
    FROM past_questions
    WHERE id = :id;
"""

GET_PAST_QUESTION_BY_UUID_QUERY = """
    SELECT * 
    FROM past_questions
    WHERE uuid = :uuid;
"""

GET_PAST_QUESTIONS_BY_COURSE_CODE_QUERY = """
    SELECT *
    FROM past_questions
    WHERE course_code = :course_code
"""

GET_PAST_QUESTIONS_BY_COURSE_NAME_QUERY = """
    SELECT *
    FROM past_questions
    WHERE course_name = :course_name
"""

GET_PAST_QUESTIONS_BY_LECTURER_QUERY = """
    SELECT *
    FROM past_questions
    WHERE lecturer = :lecturer
"""

GET_PAST_QUESTIONS_BY_SEMESTER_QUERY = """
    SELECT *
    FROM past_questions
    WHERE semester = :semester
"""

GET_PAST_QUESTIONS_BY_YEAR_QUERY = """
    SELECT *
    FROM past_questions
    WHERE year = :year
"""

GET_PAST_QUESTIONS_BY_CATEGORY_ID_QUERY = """
    SELECT *
    FROM past_questions
    WHERE category_id = :category_id
"""

GET_PAST_QUESTIONS_BY_CATEGORY_NAME_QUERY = """
    SELECT past_questions.*
    FROM past_questions
    INNER JOIN past_question_categories ON past_questions.category_id = past_question_categories.id
    WHERE past_question_categories.category_name = :category_name
"""


class PastQuestionRepository(BaseRepository):
    def __init__(self, db) -> None:
        super().__init__(db)

    async def get_past_questions_by_course_code(
        self, *, course_code: str
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by course code."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_COURSE_CODE_QUERY,
            values={"course_code": course_code},
        )
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_questions_by_course_name(
        self, *, course_name: str
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by course name."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_COURSE_NAME_QUERY,
            values={"course_name": course_name},
        )
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_questions_by_lecturer(
        self, *, lecturer: str
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by lecturer."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_LECTURER_QUERY, values={"lecturer": lecturer}
        )
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_questions_by_semester(
        self, *, semester: str
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by semester."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_SEMESTER_QUERY, values={"semester": semester}
        )
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_questions_by_year(
        self, *, year: str
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by year."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_YEAR_QUERY, values={"year": year}
        )
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_questions_by_category_id(
        self, *, category_id: int
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by category id."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_CATEGORY_ID_QUERY,
            values={"category_id": category_id},
        )
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_questions_by_category_name(
        self, *, category_name: str
    ) -> Union[List[PastQuestionInDb], None]:
        """Get past questions by category name."""
        past_questions = await self.db.fetch_all(
            query=GET_PAST_QUESTIONS_BY_CATEGORY_NAME_QUERY,
            values={"category_name": category_name},
        )

        print(past_questions)
        print("daquiver")
        if past_questions:
            return [PastQuestionInDb(**pasco) for pasco in past_questions]  # type: ignore
        return None

    async def get_past_question_by_id(
        self, *, id: int
    ) -> Union[PastQuestionInDb, None]:
        """Get past question by id."""
        past_question = await self.db.fetch_one(
            query=GET_PAST_QUESTION_BY_ID_QUERY, values={"id": id}
        )
        if past_question:
            return PastQuestionInDb(**past_question)  # type: ignore
        return None

    async def get_past_question_by_uuid(
        self, *, uuid: str
    ) -> Union[PastQuestionInDb, None]:
        """Get past question by uuid."""
        past_question = await self.db.fetch_one(
            query=GET_PAST_QUESTION_BY_UUID_QUERY, values={"uuid": uuid}
        )
        if past_question:
            return PastQuestionInDb(**past_question)  # type: ignore
        return None

    async def create_new_past_question(
        self, *, past_question: PastQuestionCreate, category_id: int
    ) -> Union[PastQuestionInDb, None]:
        uuid_ = generate_n_digit_uuid(10)
        await self.db.execute(
            query=CREATE_NEW_PAST_QUESTION_QUERY,
            values={**past_question.dict(), "category_id": category_id, "uuid": uuid_},
        )
        created_past_question = await self.get_past_question_by_uuid(uuid=uuid_)
        if created_past_question:
            return PastQuestionInDb(**created_past_question.dict())
        return None

    async def delete_past_question_by_id(self, *, id: int) -> None:
        """Delete past question by id."""
        await self.db.execute(query=DELETE_PAST_QUESTION_BY_ID_QUERY, values={"id": id})
        return None
