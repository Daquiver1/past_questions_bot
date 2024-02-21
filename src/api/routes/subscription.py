"""Route for Subscriptions"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.auth import get_current_admin, get_current_user
from src.api.dependencies.database import get_repository
from src.db.repositories.subscriptions import SubscriptionRepository
from src.db.repositories.subscriptions_history import SubscriptionHistoryRepository
from src.models.subscriptions import SubscriptionCreate, SubscriptionPublic
from src.models.subscriptions_history import SubscriptionHistoryCreate
from src.models.users import UserPublic

router = APIRouter()


@router.post(
    "",
    name="subscriptions:create-subscription",
    response_model=SubscriptionPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    subscription: SubscriptionCreate,
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    subscription_history_repo: SubscriptionHistoryRepository = Depends(
        get_repository(SubscriptionHistoryRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> SubscriptionPublic:
    """Create a new subscription."""
    new_subscription = await subscription_repo.upsert_new_subscription(
        new_subscription=subscription
    )
    if not new_subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Subscription not created."
        )
    subscription_history_create = SubscriptionHistoryCreate(
        subscription_id=new_subscription.id,
        user_telegram_id=new_subscription.user_telegram_id,
        tier=new_subscription.tier,
        amount=new_subscription.balance,
        transaction_id=new_subscription.transaction_id,
        is_active=new_subscription.is_active,
    )
    await subscription_history_repo.add_subscription_history(
        subscription_history_create=subscription_history_create
    )
    return new_subscription


@router.get(
    "/telegram",
    name="subscriptions:get-subscription-by-telegram-id",
    response_model=SubscriptionPublic,
    status_code=status.HTTP_200_OK,
)
async def get_user_subscription(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> SubscriptionPublic:
    """Get subscription details."""
    sub = await subscription_repo.get_subscription_by_user_telegram_id(
        user_telegram_id=current_user.telegram_id
    )
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub


@router.get(
    "/active",
    name="subscriptions:get-all-active-subscriptions",
    status_code=status.HTTP_200_OK,
    response_model=list[SubscriptionPublic],
)
async def get_active_subscriptions(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[SubscriptionPublic]:
    """Get all active subscriptions."""
    return await subscription_repo.get_all_active_subscriptions()


@router.get(
    "",
    name="subscriptions:get-all-subscriptions",
    status_code=status.HTTP_200_OK,
    response_model=list[SubscriptionPublic],
)
async def get_all_subscriptions(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[SubscriptionPublic]:
    """Get all subscriptions."""
    return await subscription_repo.get_all_subscriptions()


@router.patch(
    "/{balance}",
    name="subscriptions:update-subscription-balance",
    status_code=status.HTTP_200_OK,
    response_model=SubscriptionPublic,
)
async def update_subscription_balance(
    balance: int,
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> SubscriptionPublic:
    """Update subscription balance."""
    sub = await subscription_repo.update_subscription_balance(
        user_telegram_id=current_user.telegram_id, new_balance=balance
    )
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub


@router.delete(
    "",
    name="subscriptions:delete-subscription",
    status_code=status.HTTP_200_OK,
    response_model=int,
)
async def delete_subscription(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
    current_admin: UserPublic = Depends(get_current_admin),
) -> SubscriptionPublic:
    """Delete subscription."""
    return await subscription_repo.delete_subscription_by_user_telegram_id(
        user_telegram_id=current_user.telegram_id
    )
