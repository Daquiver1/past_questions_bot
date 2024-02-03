"""DB repo for help tickets."""

from typing import Optional

from databases import Database
from redis.asyncio import Redis

from src.models.help_ticket_status_enum import HelpTicketStatus
from src.db.repositories.base import BaseRepository
from src.models.help_tickets import HelpTicketsCreate, HelpTicketsInDB

ADD_HELP_TICKET_QUERY = """
    INSERT INTO help_tickets (telegram_id, subject, message, status)
    VALUES (:telegram_id, :subject, :message, :status)
    RETURNING id, telegram_id, subject, message, status, created_At, updated_At;
    """

GET_HELP_TICKET_BY_HELP_TICKET_ID_QUERY = """
    SELECT id, telegram_id, subject, message, status, created_at, updated_at
    FROM help_tickets
    WHERE id = :help_ticket_id;
    """

GET_HELP_TICKET_BY_TELEGRAM_ID_QUERY = """
    SELECT id, telegram_id, subject, message, status, created_at, updated_at
    FROM help_tickets
    WHERE telegram_id = :telegram_id;
    """

GET_ALL_HELP_TICKETS_QUERY = """
    SELECT id, telegram_id, subject, message, status, created_at, updated_at
    FROM help_tickets;
    """

UPDATE_HELP_TICKET_STATUS_QUERY = """
    UPDATE help_tickets
    SET status = :status
    WHERE id = :help_ticket_id
    RETURNING id, telegram_id, subject, message, status, created_at, updated_at;
    """

DELETE_HELP_TICKET_BY_HELP_TICKET_ID_QUERY = """
    DELETE FROM help_tickets
    WHERE id = :help_ticket_id
    RETURNING id;
    """


class HelpTicketRepository(BaseRepository):
    """All db actions associated with the help ticket resource."""

    def __init__(self, db: Database, r_db: Redis) -> None:
        """Initialize db"""
        super().__init__(db, r_db)

    async def add_new_help_ticket(
        self, *, help_ticket: HelpTicketsCreate
    ) -> HelpTicketsInDB:
        """Create new help tickets data."""
        new_help_ticket = help_ticket.copy(
            update={
                "status": HelpTicketStatus.OPEN.value,
            }
        )

        help_ticket = await self.db.fetch_one(
            query=ADD_HELP_TICKET_QUERY,
            values=new_help_ticket.dict(),
        )
        if help_ticket:
            return HelpTicketsInDB(**help_ticket)
        return None

    async def get_help_ticket_by_help_ticket_id(
        self, *, help_ticket_id: int
    ) -> Optional[HelpTicketsInDB]:
        """Get help tickets data"""
        help_ticket = await self.db.fetch_one(
            query=GET_HELP_TICKET_BY_HELP_TICKET_ID_QUERY,
            values={"help_ticket_id": help_ticket_id},
        )
        if help_ticket:
            return HelpTicketsInDB(**help_ticket)
        return None

    async def get_all_help_tickets_by_telegram_id(
        self, *, telegram_id: int
    ) -> list[HelpTicketsInDB]:
        """Get help tickets data"""
        help_tickets = await self.db.fetch_all(
            query=GET_HELP_TICKET_BY_TELEGRAM_ID_QUERY,
            values={"telegram_id": telegram_id},
        )
        if help_tickets:
            return [HelpTicketsInDB(**help_ticket) for help_ticket in help_tickets]
        return []

    async def get_all_help_tickets(self) -> list[HelpTicketsInDB]:
        """Get all help tickets data"""
        help_tickets = await self.db.fetch_all(
            query=GET_ALL_HELP_TICKETS_QUERY,
        )
        if help_tickets:
            return [HelpTicketsInDB(**help_ticket) for help_ticket in help_tickets]
        return []

    async def update_help_ticket_status(
        self, *, help_ticket_id: int, status: HelpTicketStatus
    ) -> Optional[HelpTicketsInDB]:
        """Update help tickets data"""
        help_ticket = await self.db.fetch_one(
            query=UPDATE_HELP_TICKET_STATUS_QUERY,
            values={"help_ticket_id": help_ticket_id, "status": status.value},
        )
        if help_ticket:
            return HelpTicketsInDB(**help_ticket)
        return None

    async def delete_help_ticket(self, *, help_ticket_id: int) -> int:
        """Delete help tickets data"""
        return await self.db.fetch_one(
            query=DELETE_HELP_TICKET_BY_HELP_TICKET_ID_QUERY,
            values={"help_ticket_id": help_ticket_id},
        )
