"""Paystack service test."""

from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture

from src.core.config import PAYSTACK_SECRET_KEY
from src.models.paystack import CreatePayment, CreateSubscriptionPlan
from src.services.paystack import PayStack

pytestmark = pytest.mark.asyncio


class TestPaystackFunctions:
    """Test paystack functions."""

    async def test_create_payment(
        self,
        mocker: MockerFixture,
        create_payment: CreatePayment,
        create_payment_data: dict,
    ) -> None:
        """Test creating a payment."""
        return_value = {
            "status": "success",
            "message": "Payment initialized",
            "data": {
                "authorization_url": "https://example.com/pay",
                "access_code": "ACCESS_CODE",
                "reference": "REFERENCE",
            },
        }

        mock_response = mocker.AsyncMock(
            status_code=200, json=AsyncMock(return_value=return_value)
        )
        mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

        paystack = PayStack()
        response = await paystack.create_payment(create_payment=create_payment)
        response = await response.json()

        mock_post.assert_awaited_once()
        mock_post.assert_called_once_with(
            "https://api.paystack.co/transaction/initialize",
            headers={
                "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            json=create_payment_data,
        )

        assert response["status"] == "success"
        assert "authorization_url" in response["data"]

    async def test_create_subscription_plan(
        self,
        mocker: MockerFixture,
        create_subscription_plan: CreateSubscriptionPlan,
        create_subscription_plan_data: dict,
    ) -> None:
        """Test creating a subscription plan."""
        return_value = {
            "status": "success",
            "message": "Subscription plan created",
            "data": {
                "plan_code": "PLAN_CODE",
            },
        }

        mock_response = mocker.AsyncMock(
            status_code=200, json=AsyncMock(return_value=return_value)
        )
        mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

        paystack = PayStack()
        response = await paystack.create_subscription_plan(
            create_subscription_plan=create_subscription_plan
        )
        response = await response.json()

        mock_post.assert_awaited_once()
        mock_post.assert_called_once_with(
            "https://api.paystack.co/transaction/initialize",
            headers={
                "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            },
            json=create_subscription_plan_data,
        )

        assert response["status"] == "success"
        assert "plan_code" in response["data"]

    async def test_verify_transaction(
        self,
        mocker: MockerFixture,
        reference: str,
    ) -> None:
        """Test verifying a transaction."""
        return_value = {
            "status": "success",
            "message": "Transaction retrieved",
            "data": {
                "status": "success",
                "reference": reference,
                "amount": 10000,
            },
        }

        mock_response = mocker.AsyncMock(
            status_code=200, json=AsyncMock(return_value=return_value)
        )
        mock_post = mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

        paystack = PayStack()
        response = await paystack.verify_transaction(reference=reference)
        response = await response.json()

        mock_post.assert_awaited_once()
        mock_post.assert_called_once_with(
            f"https://api.paystack.co/transaction/verify/{reference}",
            headers={
                "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            },
        )

        assert response["status"] == "success"
        assert "reference" in response["data"]
        assert response["data"]["reference"] == reference
