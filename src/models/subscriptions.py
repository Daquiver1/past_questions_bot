"""Models for subscriptions."""

from enum import Enum
from typing import Union

from pydantic import validator

from src.models.base import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin,
    UpdatedAtModelMixin,
)


class SubscriptionTier(Enum):
    """An enumeration for the subscription tier."""

    BASIC = ("Basic", 5, 7)
    STANDARD = ("Standard", 10, 15)
    PREMIUM = ("Premium", 15, 25)

    def __init__(self, tier_name: str, amount: int, questions: int) -> None:
        """Initialize the subscription tier."""
        self.tier_name = tier_name
        self.amount = amount
        self.questions = questions


class SubscriptionBase(CoreModel):
    """All common characteristics of subscription."""

    user_telegram_id: int
    tier: Union[SubscriptionTier, str]
    balance: int
    transaction_id: str
    is_active: bool = True

    @validator("tier", pre=True, allow_reuse=True)
    def convert_tier_to_enum(cls, value: str) -> SubscriptionTier:
        """Convert the tier to a SubscriptionTier enum."""
        if isinstance(value, str):
            try:
                return SubscriptionTier[value.upper()]
            except KeyError:
                raise ValueError(  # noqa
                    f"Invalid subscription tier: {value}. Choose from Basic, Standard, or Premium."
                )
        return value

    @validator("tier")
    def ensure_tier_is_enum(cls, value: str) -> SubscriptionTier:
        """Ensure the tier is a SubscriptionTier enum."""
        if not isinstance(value, SubscriptionTier):
            raise TypeError("tier must be a SubscriptionTier enum.")
        return value


class SubscriptionCreate(SubscriptionBase, UpdatedAtModelMixin):
    """Creating a new subscription."""

    pass


class SubscriptionInDB(
    IDModelMixin, DateTimeModelMixin, UpdatedAtModelMixin, SubscriptionBase
):
    """Subscription coming from DB."""

    pass


class SubscriptionPublic(SubscriptionBase, DateTimeModelMixin):
    """Subscription to public."""

    pass
