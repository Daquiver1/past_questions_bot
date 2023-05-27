"""SqlLite past question categories repository."""
from typing import Union

from db.repositories.base import BaseRepository
from models.past_question_category import PastQuestionCategoryInDb
from utils.uuid import generate_10_digit_uuid

GET_PAST_QUESTION_CATEGORY_BY_NAME_QUERY = """
    SELECT *
    FROM past_question_categories
    WHERE category_name = :category_name;
"""

DELETE_PAST_QUESTION_CATEGORY_BY_NAME_QUERY = """
    DELETE FROM past_question_categories
    WHERE category_name = :category_name;
"""

CREATE_NEW_PAST_QUESTION_CATEGORY_QUERY = """
    INSERT INTO past_question_categories (category_name,uuid)
    VALUES (:category_name,:uuid)
"""


class PastQuestionCategoriesRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def get_past_question_category_by_name(
        self, *, category_name: str
    ) -> Union[PastQuestionCategoryInDb, None]:
        """Get past question category id by name."""
        category = await self.db.fetch_one(
            query=GET_PAST_QUESTION_CATEGORY_BY_NAME_QUERY,
            values={"category_name": category_name},
        )
        if category:
            return PastQuestionCategoryInDb(**category)  # type: ignore
        return None

    async def create_new_past_question_category(
        self, *, category_name: str
    ) -> Union[PastQuestionCategoryInDb, None]:
        """Create new past question category."""
        uuid_ = generate_10_digit_uuid()

        await self.db.execute(
            query=CREATE_NEW_PAST_QUESTION_CATEGORY_QUERY,
            values={"category_name": category_name, "uuid": uuid_},
        )
        new_category = await self.get_past_question_category_by_name(
            category_name=category_name
        )
        return new_category

    async def delete_past_question_category_by_name(
        self, *, category_name: str
    ) -> None:
        """Delete past question category by name."""
        await self.db.execute(
            query=DELETE_PAST_QUESTION_CATEGORY_BY_NAME_QUERY,
            values={"category_name": category_name},
        )
        return None
