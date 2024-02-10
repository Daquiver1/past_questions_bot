"""Route for Help Tickets"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from src.api.dependencies.auth import get_current_admin, get_current_user
from src.models.users import UserPublic

from src.api.dependencies.database import get_repository
from src.db.repositories.help_tickets import HelpTicketRepository
from src.models.help_ticket_status_enum import HelpTicketStatus
from src.models.help_tickets import HelpTicketsCreate, HelpTicketsPublic

router = APIRouter()


@router.post(
    "",
    response_model=HelpTicketsPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_help_ticket(
    help_ticket: HelpTicketsCreate,
    help_ticket_repo: HelpTicketRepository = Depends(
        get_repository(HelpTicketRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> HelpTicketsPublic:
    """Create a new help ticket."""
    help_ticket = await help_ticket_repo.add_new_help_ticket(help_ticket=help_ticket)
    if not help_ticket:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Help ticket not created"
        )
    return help_ticket


@router.patch(
    "/{help_ticket_id}",
    response_model=HelpTicketsPublic,
    status_code=status.HTTP_200_OK,
)
async def update_help_ticket_status(
    help_ticket_id: int,
    help_ticket_status: HelpTicketStatus,
    help_ticket_repo: HelpTicketRepository = Depends(
        get_repository(HelpTicketRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> HelpTicketsPublic:
    """Update help ticket status."""
    help_ticket = await help_ticket_repo.update_help_ticket_status(
        help_ticket_id=help_ticket_id, status=help_ticket_status
    )
    if not help_ticket:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Help ticket not updated"
        )
    return help_ticket


@router.get(
    "{help_ticket_id}",
    response_model=Optional[HelpTicketsPublic],
    status_code=status.HTTP_200_OK,
)
async def get_help_ticket(
    help_ticket_id: int,
    help_ticket_repo: HelpTicketRepository = Depends(
        get_repository(HelpTicketRepository)
    ),
    current_user: UserPublic = Depends(get_current_user),
) -> HelpTicketsPublic:
    """Get a help ticket."""
    help_ticket = await help_ticket_repo.get_help_ticket_by_help_ticket_id(
        help_ticket_id=help_ticket_id
    )
    if not help_ticket:
        raise HTTPException(status_code=404, detail="Help ticket not found")
    return help_ticket


@router.get(
    "",
    response_model=list[HelpTicketsPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_help_tickets(
    help_ticket_repo: HelpTicketRepository = Depends(
        get_repository(HelpTicketRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[HelpTicketsPublic]:
    """Get all help tickets."""
    return await help_ticket_repo.get_all_help_tickets()


@router.get(
    "/user/{telegram_id}",
    response_model=list[HelpTicketsPublic],
    status_code=status.HTTP_200_OK,
)
async def get_all_help_tickets_by_telegram_id(
    telegram_id: int,
    help_ticket_repo: HelpTicketRepository = Depends(
        get_repository(HelpTicketRepository)
    ),
    current_admin: UserPublic = Depends(get_current_admin),
) -> list[HelpTicketsPublic]:
    """Get all help tickets by telegram id."""
    return await help_ticket_repo.get_all_help_tickets_by_telegram_id(
        telegram_id=telegram_id
    )
