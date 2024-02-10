"""Filters file."""

from aiogram.filters import Filter
from aiogram.types import Message


class TextMatchFilter(Filter):
    """A custom filter to check if the message text is equal to a given text."""

    def __init__(self, my_text: str) -> None:
        """Initialize the filter with the given text."""
        self.my_text = my_text.lower()

    async def __call__(self, message: Message) -> bool:
        """Check if the message text is equal to the given text."""
        return message.text.lower() == self.my_text


class TextStartsWithFilter(Filter):
    """A custom filter to check if the message text starts with a given text."""

    def __init__(self, my_text: str) -> None:
        """Initialize the filter with the given text."""
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        """Check if the message text starts with the given text."""
        return message.text.startswith(self.my_text)
