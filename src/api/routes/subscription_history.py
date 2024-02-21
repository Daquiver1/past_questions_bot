"""Subscription history routes."""

from fastapi import APIRouter, Depends, status

from src.api.dependencies.auth import get_current_admin, get_current_user
from src.api.dependencies.database import get_repository
from src.db.repositories.subscriptions_history import SubscriptionHistoryRepository
from src.models.subscriptions_history import SubscriptionHistoryPublic
from src.models.users import UserPublic

router = APIRouter()


@router.get(
    "/",
    response_model=list[SubscriptionHistoryPublic],
    status_code=status.HTTP_200_OK,
    name="subscription_history:get-all",
)
async def get_all_subscription_history(
    subscription_history_repo: SubscriptionHistoryRepository = Depends(
        get_repository(SubscriptionHistoryRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[SubscriptionHistoryPublic]:
    """Get all subscription history."""
    return await subscription_history_repo.get_all_subscription_history()


@router.get(
    "/subscription/{subscription_id}",
    name="subscription_history:get-all-by-subscription-id",
    status_code=status.HTTP_200_OK,
    response_model=list[SubscriptionHistoryPublic],
)
async def get_subscription_history_by_subscription_id(
    subscription_id: int,
    subscription_history_repo: SubscriptionHistoryRepository = Depends(
        get_repository(SubscriptionHistoryRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> SubscriptionHistoryPublic:
    """Get subscription history by id."""
    return (
        await subscription_history_repo.get_all_subscription_history_by_subscription_id(
            subscription_id=subscription_id
        )
    )


@router.get(
    "/telegram/",
    name="subscription_history:get-all-by-telegram-id",
    status_code=status.HTTP_200_OK,
    response_model=list[SubscriptionHistoryPublic],
)
async def get_all_subscription_history_by_telegram_id(
    subscription_history_repo: SubscriptionHistoryRepository = Depends(
        get_repository(SubscriptionHistoryRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[SubscriptionHistoryPublic]:
    """Get subscription history by telegram id."""
    return await subscription_history_repo.get_all_subscription_history_by_user_telegram_id(
        user_telegram_id=current_user.telegram_id
    )
