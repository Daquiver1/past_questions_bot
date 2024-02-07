from typing import Coroutine

import pytest
from databases import Database

from db.repositories.past_question_categories import \
    PastQuestionCategoriesRepository

pytestmark = pytest.mark.asyncio


async def test_get_past_question_category_by_name(
    db: Coroutine[None, None, Database]
) -> None:
    database = await db
    past_question_categories_repo = PastQuestionCategoriesRepository(database)
    # Create a test category in the database
    category_name = "Test Category"
    category_id = await past_question_categories_repo.create_new_past_question_category(
        category_name=category_name
    )

    # Retrieve the category ID by name
    retrieved_id = (
        await past_question_categories_repo.get_past_question_category_by_name(
            category_name=category_name
        )
    )

    # Check if the retrieved ID matches the created category ID
    assert retrieved_id == category_id


async def test_create_new_past_question_category(db: Coroutine[None, None, Database]):
    database = await db
    past_question_categories_repo = PastQuestionCategoriesRepository(database)

    # Create a new category
    category_name = "New Category"
    new_category = (
        await past_question_categories_repo.create_new_past_question_category(
            category_name=category_name
        )
    )

    # Verify that the new category is created and returned successfully
    assert new_category is not None
    assert new_category.category_name == category_name
    assert new_category.id is not None


async def test_delete_past_question_category_by_name(
    db: Coroutine[None, None, Database]
):
    database = await db
    past_question_categories_repo = PastQuestionCategoriesRepository(database)

    # Create a test past question category
    category_name = "Test Category"
    await past_question_categories_repo.create_new_past_question_category(
        category_name=category_name
    )

    # Delete the past question category by name
    await past_question_categories_repo.delete_past_question_category_by_name(
        category_name=category_name
    )

    # Verify that the past question category is deleted
    deleted_category = (
        await past_question_categories_repo.get_past_question_category_by_name(
            category_name=category_name
        )
    )
    assert deleted_category is None
