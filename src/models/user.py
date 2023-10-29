"""User Model."""

# Standard library imports
from typing import Optional

# Third party imports
from models.base import CoreModel, DateTimeModelMixin, IDModelMixin, UUIDModelMixin


class UserBase(CoreModel):
    """All common characteristics of user."""

    username: Optional[str]
    telegram_id: str
    is_subscribed: Optional[bool]
    is_eligible: Optional[bool]
    balance: Optional[float]


class UserCreate(UserBase):
    """Creating a new user."""

    pass


class UserInDb(IDModelMixin, DateTimeModelMixin, UUIDModelMixin, UserBase):
    """User coming from DB."""

    pass


class UserPublic(UserBase):
    """User to public."""

    pass
