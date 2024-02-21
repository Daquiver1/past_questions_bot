"""Route for Users"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies.auth import get_current_admin, get_current_user
from src.api.dependencies.database import get_repository
from src.db.repositories.users import UserRepository
from src.models.users import UserCreate, UserPublic

router = APIRouter()


@router.post(
    "",
    response_model=UserPublic,
    name="users:register-new-user",
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
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already created"
        )
    return user


@router.get(
    "/telegram",
    name="users:get-user-details",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
async def get_user_details(
    current_user: UserPublic = Depends(get_current_user),
) -> UserPublic:
    """Get user details."""
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


@router.get(
    "",
    name="users:get-all-users",
    response_model=list[UserPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[UserPublic]:
    """Get all users."""
    return await user_repo.get_all_users()


@router.delete(
    "/telegram",
    name="users:delete-user",
    response_model=int,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    current_admin: UserPublic = Depends(get_current_admin),
    current_user: UserPublic = Depends(get_current_user),
) -> int:
    """Delete user."""
    return await user_repo.delete_user(telegram_id=current_user.telegram_id)
