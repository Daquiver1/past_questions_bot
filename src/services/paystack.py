"""Paystack service module."""

import httpx

from src.core.config import PAYSTACK_BASE_URL, PAYSTACK_SECRET_KEY
from src.models.paystack import CreatePayment, CreateSubscriptionPlan


class PayStack:
    """A class to handle Paystack API requests."""

    def __init__(self) -> None:
        """Initialize the Paystack class."""
        self.base_url = PAYSTACK_BASE_URL
        self.secret_key = PAYSTACK_SECRET_KEY

    async def create_payment(
        self,
        create_payment: CreatePayment,
    ) -> httpx.Response:
        """This function creates a mobile money payment transaction using the Paystack API with the specified email and amount."""
        try:
            url = f"{self.base_url}transaction/initialize"
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
            }

            data = {
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
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                return response
        except Exception as e:
            print(e)

    async def create_subscription_plan(
        self,
        create_subscription_plan: CreateSubscriptionPlan,
    ) -> httpx.Response:
        """This function creates a subscription plan using the Paystack API with the specified email and amount."""
        try:
            url = f"{self.base_url}transaction/initialize"
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
            }

            data = {
                "amount": create_subscription_plan.tier.amount * 100,
                "email": "quivertech1@gmail.com",
                "currency": "GHS",
                "channels": ["mobile_money"],
                "metadata": {
                    "custom_fields": [
                        {
                            "display_name": "Telegram ID",
                            "variable_name": "Telegram ID",
                            "value": create_subscription_plan.telegram_id,
                        },
                        {
                            "display_name": "Telegram Username",
                            "variable_name": "Telegram Username",
                            "value": create_subscription_plan.telegram_username,
                        },
                        {
                            "display_name": "is_subscription",
                            "variable_name": "is_subscription",
                            "value": True,
                        },
                        {
                            "display_name": "Subscription Tier",
                            "variable_name": "Subscription Tier",
                            "value": create_subscription_plan.tier.tier_name,
                        },
                        {
                            "display_name": "Number of Questions",
                            "variable_name": "Number of Questions",
                            "value": create_subscription_plan.tier.questions,
                        },
                        {
                            "display_name": "Price",
                            "variable_name": "Price",
                            "value": create_subscription_plan.tier.amount,
                        },
                    ]
                },
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                return response

        except Exception as e:
            print(e)

    async def verify_transaction(self, reference: str) -> httpx.Response:
        """This function verifies a paystack transaction. It returns the status of the transaction."""
        try:
            url = f"{self.base_url}transaction/verify/{reference}"
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                return response
        except Exception as e:
            print(e)
