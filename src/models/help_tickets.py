"""Help Tickets Model."""

from src.models.base import CoreModel, DateTimeModelMixin, IDModelMixin
from src.models.help_ticket_status_enum import HelpTicketStatus


class HelpTicketsBase(CoreModel):
    """All common characteristics of help tickets."""

    user_telegram_id: str
    subject: str
    message: str


class HelpTicketsCreate(HelpTicketsBase):
    """Creating a new help tickets."""

    pass


class HelpTicketsInDB(HelpTicketsCreate, IDModelMixin, DateTimeModelMixin):
    """Help Tickets coming from DB."""

    status: HelpTicketStatus


class HelpTicketsPublic(HelpTicketsBase):
    """Help Tickets to public."""

    pass
