"""Route for downloads"""

from fastapi import APIRouter, Depends, HTTPException, status

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
    telegram_id: int,
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
) -> list[DownloadPublic]:
    """Get all user downloads."""
    return await download_repo.get_all_user_downloads(telegram_id=telegram_id)


@router.get(
    "/pasco/{past_question_id}",
    response_model=list[DownloadPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_past_questions_downloads(
    past_question_id: str,
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
) -> list[DownloadPublic]:
    """Get all past questions downloads."""
    return await download_repo.get_all_past_question_downloads(
        past_question_id=past_question_id
    )


@router.get("", response_model=list[DownloadPublic], status_code=status.HTTP_200_OK)
async def get_all_downloads(
    download_repo: DownloadRepository = Depends(get_repository(DownloadRepository)),
) -> list[DownloadPublic]:
    """Get all downloads."""
    return await download_repo.get_all_downloads()
