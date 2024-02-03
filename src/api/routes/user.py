"""Route for Users"""

# Third party imports

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.database import get_repository
from src.db.repositories.users import UserRepository
from src.models.users import UserCreate, UserPublic

router = APIRouter()


@router.post(
    "",
    response_model=Optional[UserPublic],
    status_code=status.HTTP_201_CREATED,
)
async def create_new_user(
    user: UserCreate,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    """Create a new user."""
    user = await user_repo.add_new_user(new_user=user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not created"
        )
    return user


@router.get(
    "/telegram/{telegram_id}",
    response_model=Optional[UserPublic],
    status_code=status.HTTP_200_OK,
)
async def get_user_details(
    telegram_id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    """Get user details."""
    user = await user_repo.get_user_details(telegram_id=telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "",
    response_model=list[UserPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> list[UserPublic]:
    """Get all users."""
    return await user_repo.get_all_users()


@router.delete(
    "/telegram/{telegram_id}",
    response_model=Optional[int],
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    telegram_id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> int:
    """Delete user."""
    telegram_id = await user_repo.delete_user(telegram_id=telegram_id)

    if not telegram_id:
        raise HTTPException(status_code=404, detail="User not found")
    return telegram_id
