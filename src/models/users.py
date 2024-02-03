"""User Model."""

# Standard library imports
from typing import Optional

# Third party imports
from src.models.base import CoreModel, DateTimeModelMixin


class UserBase(CoreModel):
    """All common characteristics of user."""

    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    telegram_id: int


class UserCreate(UserBase):
    """Creating a new user."""

    pass


class UserInDB(DateTimeModelMixin, UserBase):
    """User coming from DB."""

    pass


class UserPublic(UserBase):
    """User to public."""

    pass
