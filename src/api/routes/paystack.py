"""Route to accept user payments."""

import hashlib
import hmac

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

from src.core.config import PAYSTACK_SECRET_KEY
from src.models.paystack import (
    CreatePayment,
    CreatePaymentResponse,
    CreateSubscriptionPlan,
    SuccessfulTransaction,
    VerifyTransaction,
)
from src.services.paystack import PayStack

router = APIRouter()
paystack = PayStack()
BASIC_PLAN = 5
STANDARD_PLAN = 10
PREMIUM_PLAN = 15


@router.post(
    "/create_payment",
    response_model=CreatePaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    create_payment: CreatePayment,
) -> CreatePaymentResponse:
    """This function creates a mobile money payment transaction using the Paystack API with the specified email and amount."""
    try:
        response = await paystack.create_payment(create_payment)
        if response.status_code == 200 and response.json()["status"] is True:
            print(response.json())
            return response.json()["data"]
        else:
            return response.json()
    except Exception as e:
        print(e)


@router.get(
    "/verify_transaction/{reference}",
    response_model=VerifyTransaction,
)
async def verify_transaction(reference: str) -> VerifyTransaction:
    """This function verifies a paystack transaction. It returns the status of the transaction."""
    try:
        response = await paystack.verify_transaction(reference)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print(e)


@router.post("/create_subscription", status_code=status.HTTP_201_CREATED)
async def create_subscribe_plan(
    create_subscription_plan: CreateSubscriptionPlan,
) -> CreatePaymentResponse:
    """Endpoint for the Basic tier subscription."""
    try:
        response = await paystack.create_subscription_plan(create_subscription_plan)
        if response:
            if response.status_code == 200 and response.json()["status"] is True:
                return response.json()["data"]
            else:
                return response.json()
        else:
            return response
    except Exception as e:
        print(e)


@router.get("/verify_subscription/{reference}")
async def verify_subscription(reference: str) -> VerifyTransaction:
    """This function verifies a paystack transaction. It returns the status of the transaction."""
    try:
        response = await paystack.verify_transaction(reference)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print(e)


@router.post("/webhook")
async def paystack_webhook(request: Request, response: Response) -> JSONResponse:
    """This function creates a webhook, that'll receive a response from Paystack."""
    payload = await request.body()
    signature = request.headers.get("x-paystack-signature")

    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(), msg=payload, digestmod=hashlib.sha512
    ).hexdigest()

    if signature != computed_signature:
        return JSONResponse(content={"message": "Invalid signature"}, status_code=404)

    event = await request.json()

    print(event)
    response = SuccessfulTransaction(**event["data"])
    print(response)

    return JSONResponse(
        content={"message": "Transaction was successful."}, status_code=200
    )
