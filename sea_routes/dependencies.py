from typing import Annotated

from fastapi import Depends

from sea_routes.repositorites import SeaRoutesRepository


def get_sea_routes_repo() -> SeaRoutesRepository:
    return SeaRoutesRepository()


SeaRoutesRepo = Annotated[SeaRoutesRepository, Depends(get_sea_routes_repo)]
