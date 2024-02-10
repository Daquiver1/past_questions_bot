"""Core data that exist in all Models."""

# Standard library imports
from datetime import datetime
from typing import Optional

# Third party imports
from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    """Any common logic to be shared by all models."""

    pass


class IDModelMixin(BaseModel):
    """ID data."""

    id: int


class UUIDModelMixin(BaseModel):
    """UUID data."""

    uuid: str


class DateTimeModelMixin(BaseModel):
    """Datetime model data."""

    created_at: Optional[datetime]


class UpdatedAtModelMixin(BaseModel):
    """Updated at model data."""

    updated_at: Optional[datetime] = datetime.now()

    @validator("updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        """Validate both created_at and update_at data."""
        return datetime.now()
