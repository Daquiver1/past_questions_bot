"""Models for the application."""

from enum import Enum
from typing import Any, Optional


class SubscriptionTier(Enum):
    """Enum for the subscription tiers."""

    BASIC = ("Basic", 5, 7)
    STANDARD = ("Standard", 10, 15)
    PREMIUM = ("Premium", 15, 25)

    def __init__(self, tier_name: str, amount: int, questions: int) -> None:
        """Initialize the subscription tier."""
        self.tier_name = tier_name
        self.amount = amount
        self.questions = questions

    @classmethod
    def from_arg(cls, arg: str):
        """Get the subscription tier from the argument."""
        arg = arg.lower()
        for tier in cls:
            if tier.name.lower() == arg:
                return tier
        return None
