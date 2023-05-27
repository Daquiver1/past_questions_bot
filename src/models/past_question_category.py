"""Model for past question category."""

from typing import Optional

from models.base import CoreModel, DateTimeModelMixin, IDModelMixin, UUIDModelMixin


class PastQuestionCategoryBase(CoreModel):
    """All common characteristics of past question category."""

    category_name: Optional[str]


class PastQuestionCategoryCreate(PastQuestionCategoryBase):
    """Creating a new past question category."""

    pass


class PastQuestionCategoryInDb(
    IDModelMixin, DateTimeModelMixin, UUIDModelMixin, PastQuestionCategoryBase
):
    """Past Question category coming from DB."""

    pass


class PastQuestionCategoryPublic(PastQuestionCategoryBase):
    """Past Question category Public."""

    pass
