"""Route to accept user payments."""

import hashlib
import hmac

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.database import get_repository
from src.core.config import PAYSTACK_SECRET_KEY
from src.db.repositories.subscriptions import SubscriptionRepository
from src.models.paystack import (
    CreatePayment,
    CreatePaymentResponse,
    CreateSubscriptionPlan,
    SuccessfulTransaction,
    VerifyTransaction,
)
from src.models.subscriptions import SubscriptionCreate
from src.models.users import UserPublic
from src.services.paystack import PayStack

router = APIRouter()
paystack = PayStack()


@router.post(
    "/create_payment",
    response_model=CreatePaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    create_payment: CreatePayment,
    current_user: UserPublic = Depends(get_current_user),
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
async def verify_transaction(
    reference: str,
    current_user: UserPublic = Depends(get_current_user),
) -> VerifyTransaction:
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
    current_user: UserPublic = Depends(get_current_user),
) -> CreatePaymentResponse:
    """Endpoint for the subscription."""
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
async def verify_subscription(
    reference: str,
    current_user: UserPublic = Depends(get_current_user),
) -> VerifyTransaction:
    """This function verifies a paystack transaction. It returns the status of the transaction."""
    try:
        response = await paystack.verify_transaction(reference)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except Exception as e:
        print(e)


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def paystack_webhook(
    request: Request,
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
) -> JSONResponse:
    """This function creates a webhook, that'll receive a response from Paystack."""
    payload = await request.body()
    signature = request.headers.get("x-paystack-signature")

    # Verify signature
    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode(), msg=payload, digestmod=hashlib.sha512
    ).hexdigest()

    if signature != computed_signature:
        return JSONResponse(content={"message": "Invalid signature"}, status_code=400)

    event = await request.json()
    transaction_data = SuccessfulTransaction(**event["data"])

    is_subscription = False
    user_telegram_id = None
    telegram_username = None
    tier = None
    balance = None
    print(transaction_data.metadata.custom_fields)
    for custom_field in transaction_data.metadata.custom_fields:
        if (
            custom_field.variable_name == "is_subscription"
            and custom_field.value == "true"
        ):
            is_subscription = True
        elif custom_field.variable_name == "Telegram ID":
            user_telegram_id = int(custom_field.value)
        elif custom_field.variable_name == "Telegram Username":
            telegram_username = custom_field.value
        elif custom_field.variable_name == "Subscription Tier":
            tier = custom_field.value
        elif custom_field.variable_name == "Price":
            balance = int(custom_field.value)

    print(is_subscription, user_telegram_id, telegram_username, tier, balance)

    if is_subscription and all([user_telegram_id, telegram_username, tier, balance]):
        create_subscription_data = SubscriptionCreate(
            user_telegram_id=user_telegram_id,
            telegram_username=telegram_username,
            transaction_id=transaction_data.reference,
            balance=balance,
            tier=tier,
        )
        sub = await subscription_repo.upsert_new_subscription(
            new_subscription=create_subscription_data
        )
        if sub:
            return JSONResponse(
                content={"message": "Subscription created successfully"},
                status_code=200,
            )
        else:
            return JSONResponse(
                content={"message": "Error creating subscription"}, status_code=400
            )
    else:
        return JSONResponse(
            content={"message": "Transaction processed but not a subscription."},
            status_code=200,
        )
