"""Downloads Model"""

from src.models.base import CoreModel, DateTimeModelMixin, IDModelMixin


class DownloadBase(CoreModel):
    """All common characteristics of downloads."""

    user_id: str
    past_question_id: int


class DownloadCreate(DownloadBase):
    """Creating a new downloads."""

    pass


class DownloadInDB(DownloadCreate, IDModelMixin, DateTimeModelMixin):
    """Downloads coming from DB."""

    pass


class DownloadPublic(DownloadBase):
    """Downloads to public."""

    pass
