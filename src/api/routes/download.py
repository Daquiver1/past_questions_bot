"""Route for downloads"""

from fastapi import APIRouter, Depends, HTTPException, status
from telegram import User

from src.api.dependencies.auth import get_current_admin, get_current_user
from src.models.users import UserPublic
from src.api.dependencies.database import get_repository
from src.db.repositories.downloads import DownloadRepository
from src.models.downloads import DownloadCreate, DownloadPublic

router = APIRouter()


@router.post(
    "",
    response_model=DownloadPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_download(
    download: DownloadCreate,
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
    current_user: User = Depends(get_current_user),
) -> DownloadPublic:
    """Create a new download."""
    download = await download_repo.add_new_download(new_download=download)
    if not download:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Download not created"
        )
    return download


@router.get(
    "/user/{telegram_id}",
    response_model=list[DownloadPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_user_downloads(
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
    current_user: UserPublic = Depends(get_current_user),
) -> list[DownloadPublic]:
    """Get all user downloads."""
    return await download_repo.get_all_user_downloads(
        telegram_id=current_user.telegram_id
    )


@router.get(
    "/pasco/{past_question_id}",
    response_model=list[DownloadPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_past_questions_downloads(
    past_question_id: str,
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[DownloadPublic]:
    """Get all past questions downloads."""
    return await download_repo.get_all_past_question_downloads(
        past_question_id=past_question_id
    )


@router.get("", response_model=list[DownloadPublic], status_code=status.HTTP_200_OK)
async def get_all_downloads(
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[DownloadPublic]:
    """Get all downloads."""
    return await download_repo.get_all_downloads()
