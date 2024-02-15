"""Paystack fixtures for testing paystack."""

import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))
from src.models.paystack import CreatePayment, CreateSubscriptionPlan


@pytest.fixture
def create_payment() -> CreatePayment:
    """Return create payment data"""
    return CreatePayment(telegram_id=10829273, telegram_username="test", amount=100)


@pytest.fixture
def create_payment_data(create_payment: CreatePayment) -> dict:
    """Return create payment data"""
    return {
        "amount": create_payment.amount * 100,
        "email": "quivertech1@gmail.com",
        "currency": "GHS",
        "channels": ["mobile_money"],
        "metadata": {
            "custom_fields": [
                {
                    "display_name": "Telegram ID",
                    "variable_name": "Telegram ID",
                    "value": create_payment.telegram_id,
                },
                {
                    "display_name": "Telegram Username",
                    "variable_name": "Telegram Username",
                    "value": create_payment.telegram_username,
                },
                {
                    "display_name": "is_subscription",
                    "variable_name": "is_subscription",
                    "value": False,
                },
            ]
        },
    }


@pytest.fixture
def create_subscription_plan() -> CreateSubscriptionPlan:
    """Return create subscription data"""
    return CreateSubscriptionPlan(
        telegram_id=10829272,
        telegram_username="test",
        tier="Basic",
    )


@pytest.fixture
def reference() -> str:
    """Return reference data for paystack."""
    return "test"


@pytest.fixture
def create_subscription_plan_data() -> dict:
    """Return subscription data"""
    return {
        "amount": 5 * 100,
        "email": "quivertech1@gmail.com",
        "currency": "GHS",
        "channels": ["mobile_money"],
        "metadata": {
            "custom_fields": [
                {
                    "display_name": "Telegram ID",
                    "variable_name": "Telegram ID",
                    "value": 10829272,
                },
                {
                    "display_name": "Telegram Username",
                    "variable_name": "Telegram Username",
                    "value": "test",
                },
                {
                    "display_name": "is_subscription",
                    "variable_name": "is_subscription",
                    "value": True,
                },
                {
                    "display_name": "Subscription Tier",
                    "variable_name": "Subscription Tier",
                    "value": "Basic",
                },
                {
                    "display_name": "Number of Questions",
                    "variable_name": "Number of Questions",
                    "value": 7,
                },
                {
                    "display_name": "Price",
                    "variable_name": "Price",
                    "value": 5,
                },
            ]
        },
    }
