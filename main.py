from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic_geojson import FeatureCollectionModel

from dependencies import SQLiteRepository
from models import RouteModel

app = FastAPI()


@app.get("/routes")
def get_all_routes(db_repo: SQLiteRepository) -> list[RouteModel]:
    return db_repo.get_all_routes()


@app.get("/routes/{route_id}")
def get_route(
    route_id: int, db_repo: SQLiteRepository
) -> Optional[FeatureCollectionModel]:
    route = db_repo.get_route(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="No route id found")
    return route
