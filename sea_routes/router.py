from fastapi import APIRouter
from pydantic_geojson import FeatureCollectionModel

from sea_routes.dependencies import SeaRoutesRepo
from sea_routes.models import RouteModel

sea_routes_router = APIRouter()


@sea_routes_router.get("/routes")
async def get_all_routes(db_repo: SeaRoutesRepo) -> list[RouteModel]:
    return await db_repo.get_all_routes()


@sea_routes_router.get("/routes/{route_id}")
async def get_route(route_id: int, db_repo: SeaRoutesRepo) -> FeatureCollectionModel:
    return await db_repo.get_route(route_id)
