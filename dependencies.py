from typing import Annotated

from fastapi import Depends

from sqlite_repository import SqliteRepository


def get_sqlite_repo() -> SqliteRepository:
    return SqliteRepository()


SQLiteRepository = Annotated[SqliteRepository, Depends(get_sqlite_repo)]
