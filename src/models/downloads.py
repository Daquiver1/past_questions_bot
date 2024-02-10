"""Downloads Model"""

from src.models.base import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin,
    UpdatedAtModelMixin,
)


class DownloadBase(CoreModel):
    """All common characteristics of downloads."""

    user_telegram_id: int
    past_question_id: int


class DownloadCreate(DownloadBase, UpdatedAtModelMixin):
    """Creating a new downloads."""

    pass


class DownloadInDB(
    DownloadCreate, IDModelMixin, UpdatedAtModelMixin, DateTimeModelMixin
):
    """Downloads coming from DB."""

    pass


class DownloadPublic(DownloadBase):
    """Downloads to public."""

    pass
