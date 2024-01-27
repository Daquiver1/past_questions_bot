"""Past Question Model"""
from src.models.base import CoreModel, DateTimeModelMixin, IDModelMixin


class PastQuestionBase(CoreModel):
    """All common characteristics of past question."""

    course_code: str
    course_name: str
    lecturer_name: str
    semester: str
    year: str
    past_question_url: str


class PastQuestionCreate(PastQuestionBase):
    """Creating a new past question."""

    pass


class PastQuestionInDB(IDModelMixin, DateTimeModelMixin, PastQuestionBase):
    """Past Question coming from DB."""

    pass


class PastQuestionPublic(PastQuestionBase):
    """Past Question Public."""

    pass
