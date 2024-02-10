from typing import Coroutine

import pytest
from databases import Database

from db.repositories.past_question import PastQuestionRepository
from db.repositories.past_question_categories import \
    PastQuestionCategoriesRepository
from models.past_questions import PastQuestionCreate

pytestmark = pytest.mark.asyncio


async def test_get_past_questions_by_course_code(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db  # db is received as a coroutine so we need to await it
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by course code
    past_questions = await past_question_repo.get_past_questions_by_course_code(
        course_code=str(new_past_question.course_code)
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].course_code == new_past_question.course_code


async def test_get_past_questions_by_course_name(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by course name
    past_questions = await past_question_repo.get_past_questions_by_course_name(
        course_name=str(new_past_question.course_name)
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].course_name == new_past_question.course_name


async def test_get_past_questions_by_semester(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by semester
    past_questions = await past_question_repo.get_past_questions_by_semester(
        semester=str(new_past_question.semester)
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].semester == new_past_question.semester


async def test_get_past_questions_by_year(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by year
    past_questions = await past_question_repo.get_past_questions_by_year(
        year=str(new_past_question.year)
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].year == new_past_question.year


async def test_get_past_questions_by_lecturer(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by lecturer
    past_questions = await past_question_repo.get_past_questions_by_lecturer(
        lecturer=str(new_past_question.lecturer)
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].lecturer == new_past_question.lecturer


async def test_get_past_questions_by_category_id(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by category ID
    past_questions = await past_question_repo.get_past_questions_by_category_id(
        category_id=category_id
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].category_id == category_id


async def test_get_past_questions_by_category_name(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)
    past_question_categories_repo = PastQuestionCategoriesRepository(database)

    # Create a test past question category
    category_name = "DCIT"
    category = await past_question_categories_repo.create_new_past_question_category(
        category_name=category_name
    )
    assert category is not None

    category_id = 1
    category_name = "DCIT"
    await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )

    # Get past questions by category name
    past_questions = await past_question_repo.get_past_questions_by_category_name(
        category_name=category_name
    )

    # Verify that the past question is returned
    assert past_questions is not None
    assert len(past_questions) == 1
    assert past_questions[0].course_code is not None
    assert category_name in past_questions[0].course_code


async def test_get_past_question_by_id(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    created_past_question = await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )
    assert created_past_question is not None

    # Get the past question by ID
    past_question = await past_question_repo.get_past_question_by_id(
        id=created_past_question.id
    )

    # Verify that the past question is returned
    assert past_question is not None
    assert past_question.id == created_past_question.id


async def test_delete_past_question_by_id(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    # Create a test past question
    database = await db
    past_question_repo = PastQuestionRepository(database)

    category_id = 1
    created_past_question = await past_question_repo.create_new_past_question(
        past_question=new_past_question, category_id=category_id
    )
    assert created_past_question is not None

    # Delete the past question
    await past_question_repo.delete_past_question_by_id(id=created_past_question.id)

    # Try to retrieve the deleted past question
    deleted_past_question = await past_question_repo.get_past_question_by_id(
        id=created_past_question.id
    )

    # Verify that the past question is deleted (should return None)
    assert deleted_past_question is None


async def test_create_new_past_question(
    db: Coroutine[None, None, Database], new_past_question: PastQuestionCreate
):
    database = await db
    past_question_repo = PastQuestionRepository(database)
    past_question_categories_repo = PastQuestionCategoriesRepository(database)

    # Create a test past question category
    category_name = "Test Category"
    category = await past_question_categories_repo.create_new_past_question_category(
        category_name=category_name
    )
    assert category is not None

    created_past_question = await past_question_repo.create_new_past_question(
        past_question=new_past_question,
        category_id=category.id,
    )

    # Verify that the past question is created and has the correct values
    assert created_past_question is not None
    assert created_past_question.course_code == new_past_question.course_code
