"""Dependency for db."""

# Standard library imports
from typing import Callable, Type, Union

# Third party imports
from databases import Database
from fastapi import Depends

from src.db.repositories.base import BaseRepository
from starlette.requests import Request


def get_database(request: Request) -> Database:
    """Get db from app state."""
    return request.app.state._db


def get_repository(repo_type: Union[Type[BaseRepository], BaseRepository]) -> Callable:
    """Dependency for db."""

    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return repo_type(db)  # type: ignore

    return get_repo
