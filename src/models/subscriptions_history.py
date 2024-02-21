"""Subscription history model."""

from typing import Union

from pydantic import field_validator

from src.models.base import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin,
    UpdatedAtModelMixin,
)
from src.models.subscriptions import SubscriptionTier


class SubscriptionHistoryBase(CoreModel):
    """All common characteristics of subscription history."""

    user_telegram_id: int
    subscription_id: int
    tier: Union[SubscriptionTier, str]
    amount: int
    transaction_id: str
    is_active: bool = True

    @field_validator(
        "tier",
    )
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

    @field_validator("tier")
    def ensure_tier_is_enum(cls, value: str) -> SubscriptionTier:
        """Ensure the tier is a SubscriptionTier enum."""
        if not isinstance(value, SubscriptionTier):
            raise TypeError("tier must be a SubscriptionTier enum.")
        return value


class SubscriptionHistoryCreate(SubscriptionHistoryBase, UpdatedAtModelMixin):
    """Properties to receive on subscription history creation."""

    pass


class SubscriptionHistoryInDB(
    IDModelMixin, DateTimeModelMixin, UpdatedAtModelMixin, SubscriptionHistoryBase
):
    """Properties to receive on subscription history update."""

    pass


class SubscriptionHistoryPublic(SubscriptionHistoryBase, DateTimeModelMixin):
    """Subscription history properties to return to client."""

    pass
