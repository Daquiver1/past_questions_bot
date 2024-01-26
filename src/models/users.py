"""User Model."""

# Standard library imports
from typing import Optional

# Third party imports
from src.models.base import CoreModel, DateTimeModelMixin, IDModelMixin, UUIDModelMixin


class UserBase(CoreModel):
    """All common characteristics of user."""

    username: Optional[str]
    first_name: str
    last_name: str
    telegram_id: str


class UserCreate(UserBase):
    """Creating a new user."""

    pass


class UserInDB(IDModelMixin, DateTimeModelMixin, UUIDModelMixin, UserBase):
    """User coming from DB."""

    pass


class UserPublic(UserBase):
    """User to public."""

    pass
