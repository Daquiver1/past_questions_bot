"""Add updated at to model."""
from datetime import datetime

from pydantic import BaseModel

def add_updated_at(model: BaseModel) -> BaseModel:
    """Add updated at to model."""
    model_copy = model.copy(update={"updated_at": datetime.now(timezone.utc)})

    model.updated_at = datetime.now()
    return model