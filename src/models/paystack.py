"""Model for paystack."""

from typing import List, Union

from pydantic import validator

from src.models.base import CoreModel, IDModelMixin
from src.models.subscriptions import SubscriptionTier


class CustomField(CoreModel):
    """Custom field for paystack."""

    display_name: str
    variable_name: str
    value: str


class Metadata(CoreModel):
    """Metadata for paystack."""

    custom_fields: List[CustomField]


class CreatePaymentResponse(CoreModel):
    """A model for the response of creating a payment."""

    authorization_url: str
    access_code: str
    reference: str


class CreatePayment(CoreModel):
    """A model for creating payment."""

    telegram_id: int
    telegram_username: str
    amount: float


class CreateSubscriptionPlan(CoreModel):
    """A model for creating a subscription plan."""

    telegram_id: int
    telegram_username: str
    tier: Union[SubscriptionTier, str]

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


class VerifyTransaction(CoreModel):
    """A model for verifying the transaction."""

    status: bool
    message: str
    data: dict


class SuccessfulTransaction(CoreModel, IDModelMixin):
    """A model for a successful transaction."""

    status: str
    reference: str
    amount: int
    paid_at: str
    created_at: str
    metadata: Metadata

    @validator("amount", pre=True, allow_reuse=True)
    def divide_amount_by_100(cls, v: int) -> float:
        """Divide the amount by 100."""
        return v / 100
