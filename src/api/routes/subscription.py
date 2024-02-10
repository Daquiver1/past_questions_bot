"""Route for Subscriptions"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.auth import get_current_admin, get_current_user
from src.api.dependencies.database import get_repository
from src.db.repositories.subscriptions import SubscriptionRepository
from src.models.subscriptions import SubscriptionCreate, SubscriptionPublic
from src.models.users import UserPublic

router = APIRouter()


@router.post(
    "",
    response_model=SubscriptionPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    subscription: SubscriptionCreate,
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> SubscriptionPublic:
    """Create a new subscription."""
    sub = await subscription_repo.upsert_new_subscription(new_subscription=subscription)
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Subscription not created."
        )
    return sub


@router.get("/telegram", response_model=SubscriptionPublic)
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


@router.get("/active", response_model=list[SubscriptionPublic])
async def get_active_subscriptions(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[SubscriptionPublic]:
    """Get all active subscriptions."""
    return await subscription_repo.get_all_active_subscriptions()


@router.get("", response_model=list[SubscriptionPublic])
async def get_all_subscriptions(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[SubscriptionPublic]:
    """Get all subscriptions."""
    return await subscription_repo.get_all_subscriptions()


@router.patch("/{balance}", response_model=SubscriptionPublic)
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


@router.delete("", response_model=SubscriptionPublic)
async def delete_subscription(
    subscription_repo: SubscriptionRepository = Depends(
        get_repository(SubscriptionRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
    current_admin: UserPublic = Depends(get_current_admin),
) -> SubscriptionPublic:
    """Delete subscription."""
    sub = await subscription_repo.delete_subscription_by_user_telegram_id(
        user_telegram_id=current_user.telegram_id
    )
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return sub
