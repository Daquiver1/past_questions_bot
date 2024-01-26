"""Route for accessing past questions."""

from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.past_questions import PastQuestionRepository
from src.models.past_questions import PastQuestionCreate, PastQuestionPublic
from src.models.past_question_filter_enum import PastQuestionFilter

router = APIRouter()


@router.post(
    "",
    response_model=Optional[PastQuestionPublic],
    status_code=status.HTTP_201_CREATED,
)
async def create_new_past_question(
    past_question: PastQuestionCreate,
    past_question_repo: PastQuestionRepository = Depends(
        get_repository(PastQuestionRepository)
    ),
) -> PastQuestionPublic:
    """Create a new past question."""
    past_question = await past_question_repo.add_new_past_question(
        new_past_question=past_question
    )
    if not past_question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Past question not created"
        )
    return past_question


@router.get(
    "/{past_question_id}",
    response_model=Optional[PastQuestionPublic],
    status_code=status.HTTP_200_OK,
)
async def get_past_question(
    past_question_id: int,
    past_question_repo: PastQuestionRepository = Depends(
        get_repository(PastQuestionRepository)
    ),
) -> PastQuestionPublic:
    """Get a past question"""
    past_question = await past_question_repo.get_past_question(
        filter_by="past_question_id", filter_value=past_question_id
    )
    if not past_question:
        raise HTTPException(status_code=404, detail="Past question not found")
    return past_question


@router.get(
    "",
    response_model=list[PastQuestionPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_past_questions(
    past_question_repo: PastQuestionRepository = Depends(
        get_repository(PastQuestionRepository)
    ),
) -> list[PastQuestionPublic]:
    """Get all past questions."""
    return await past_question_repo.get_all_past_questions()


@router.get(
    "/filter_by/{filter_by}/{filter_value}",
    response_model=list[PastQuestionPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_past_questions_by_filter(
    filter_by: PastQuestionFilter,
    filter_value: Union[int, str],
    past_question_repo: PastQuestionRepository = Depends(
        get_repository(PastQuestionRepository)
    ),
) -> list[PastQuestionPublic]:
    """Get all past questions by filter."""
    return await past_question_repo.get_all_past_questions_by_filter(
        filter_by=filter_by, filter_value=filter_value
    )
