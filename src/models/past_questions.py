"""Past Question Model"""

from typing import Optional

from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from src.models.base import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin,
    UpdatedAtModelMixin,
)


class PastQuestionBase(CoreModel):
    """All common characteristics of past question."""

    course_code: str
    course_name: str
    course_title: Optional[str]
    lecturer_name: str
    semester: str
    year: str
    past_question_url: Optional[str]

    @field_validator("course_name")
    def validate_course_name(cls, v: str) -> str:
        """Validate course name."""
        v = v.strip()
        if len(v) != 4 or not v.isalpha():
            raise ValueError("course_name must be 4 characters")
        return v.lower()

    @field_validator("course_code")
    def validate_course_code(cls, v: str) -> str:
        """Validate course code."""
        v = v.strip()
        if len(v) != 3 or not v.isnumeric():
            raise ValueError("course_code must be 3 characters")
        return v.lower()

    @field_validator("course_title")
    def set_course_title(
        cls, v: Optional[str], info: ValidationInfo, **kwargs: any
    ) -> str:
        """Set course title."""
        course_name = info.data["course_name"]
        course_code = info.data["course_code"]
        if course_name and course_code:
            return f"{course_name} {course_code}"
        elif v:
            return v.strip().lower()
        raise ValueError("course_title cannot be generated")


class PastQuestionCreate(PastQuestionBase, UpdatedAtModelMixin):
    """Creating a new past question."""

    pass


class PastQuestionInDB(
    IDModelMixin, DateTimeModelMixin, UpdatedAtModelMixin, PastQuestionBase
):
    """Past Question coming from DB."""

    hash_key: str


class PastQuestionPublic(IDModelMixin, PastQuestionBase):
    """Past Question Public."""

    hash_key: str
