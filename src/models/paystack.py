"""Model for paystack."""

from typing import List

from pydantic import validator

from src.models.base import CoreModel, IDModelMixin


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
    def divide_amount_by_100(cls, v) -> float:
        """Divide the amount by 100."""
        return v / 100
