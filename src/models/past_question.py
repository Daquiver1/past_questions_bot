"""Past Question Model"""

from typing import Optional

from models.base import CoreModel, DateTimeModelMixin, IDModelMixin, UUIDModelMixin


class PastQuestionBase(CoreModel):
    """All common characteristics of past question."""

    course_code: Optional[str]
    course_name: Optional[str]
    lecturer: Optional[str]
    past_question_url: Optional[str]
    semester: Optional[str]
    year: Optional[str]


class PastQuestionCreate(PastQuestionBase):
    """Creating a new past question."""

    pass


class PastQuestionInDb(
    IDModelMixin, DateTimeModelMixin, UUIDModelMixin, PastQuestionBase
):
    """Past Question coming from DB."""

    category_id: Optional[int]


class PastQuestionPublic(PastQuestionBase):
    """Past Question Public."""

    pass
