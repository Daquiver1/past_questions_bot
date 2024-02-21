"""Dependency for authentication."""

# Third party imports
from fastapi import Depends, Header, HTTPException, status

from src.api.dependencies.database import get_repository
from src.core.config import ADMIN_TELEGRAM_ID
from src.db.repositories.users import UserRepository
from src.models.users import UserPublic


async def get_telegram_id_from_header(x_telegram_id: str = Header(None)) -> int:
    """Get Telegram ID from header."""
    if x_telegram_id is None:
        raise HTTPException(status_code=400, detail="X-Telegram-ID header missing")
    try:
        return int(x_telegram_id)
    except ValueError:
        raise HTTPException(  # noqa
            status_code=400, detail="Invalid X-Telegram-ID header value"
        )


async def get_admin_telegram_id_from_header(x_admin_telegram_id: str = Header(None)) -> int:
    """Get Telegram ID from header."""
    if x_admin_telegram_id is None:
        raise HTTPException(status_code=400, detail="Admin telegram id header missing")
    try:
        return int(x_admin_telegram_id)
    except ValueError:
        raise HTTPException(  # noqa
            status_code=400, detail="Invalid X-Telegram-ID header value"
        )


async def get_current_user(
    telegram_id: int = Depends(get_telegram_id_from_header),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    """Get current active user based on Telegram ID."""
    client = await user_repo.get_user_details(telegram_id=telegram_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please register to use the service.",
        )
    return client


async def get_current_admin(
    telegram_id: int = Depends(get_admin_telegram_id_from_header),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> UserPublic:
    """Get current active admin based on Telegram ID."""
    client = await user_repo.get_user_details(telegram_id=telegram_id)
    if not client or client.telegram_id != ADMIN_TELEGRAM_ID:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Only admin can access this endpoint.",
        )
    return client
