"""Enum for the status of a help ticket."""

from enum import Enum


class HelpTicketStatus(Enum):
    """Enum for the status of a help ticket."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
