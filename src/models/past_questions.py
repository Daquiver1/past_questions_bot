"""Past Question Model"""
from src.models.base import CoreModel, DateTimeModelMixin, IDModelMixin
from pydantic import validator
from typing import Optional


class PastQuestionBase(CoreModel):
    """All common characteristics of past question."""

    course_code: str
    course_name: str
    course_title: Optional[str]
    lecturer_name: str
    semester: str
    year: str
    past_question_url: Optional[str]

    @validator("course_name")
    def validate_course_name(cls, v: str) -> str:
        """Validate course name."""
        v = v.strip()
        if len(v) != 4 or not v.isalpha():
            raise ValueError("course_name must be 4 characters")
        return v.lower()

    @validator("course_code")
    def validate_course_code(cls, v: str) -> str:
        """Validate course code."""
        v = v.strip()
        if len(v) != 3 or not v.isnumeric():
            raise ValueError("course_code must be 3 characters")
        return v.lower()

    @validator("course_title", pre=True, always=True)
    def set_course_title(cls, v: Optional[str], values: dict, **kwargs: any) -> str:
        """Set course title."""
        course_name = values.get("course_name")
        course_code = values.get("course_code")
        if course_name and course_code:
            return f"{course_name} {course_code}"
        elif v:
            return v.strip().lower()
        raise ValueError("course_title cannot be generated")


class PastQuestionCreate(PastQuestionBase):
    """Creating a new past question."""

    pass


class PastQuestionInDB(IDModelMixin, DateTimeModelMixin, PastQuestionBase):
    """Past Question coming from DB."""

    pass


class PastQuestionPublic(IDModelMixin, PastQuestionBase):
    """Past Question Public."""

    pass
