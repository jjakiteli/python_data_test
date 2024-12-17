import json

from pydantic_geojson import FeatureCollectionModel, FeatureModel, PointModel
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from sea_routes.exceptions import RouteNotFoundException
from sea_routes.models import Route, RouteModel

DATABASE_URL = "sqlite+aiosqlite:///./db/sea_routes.db"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class SeaRoutesRepository:
    def __init__(self):
        self.session_factory = SessionLocal

    async def get_all_routes(self) -> list[RouteModel]:
        async with self.session_factory() as session:
            query = select(Route)
            result = await session.execute(query)
            routes = result.scalars().all()
            return [
                RouteModel(
                    route_id=route.id,
                    from_port=route.from_port,
                    to_port=route.to_port,
                    leg_duration=route.leg_duration,
                )
                for route in routes
            ]

    async def get_route(self, id: int) -> FeatureCollectionModel:
        async with self.session_factory() as session:
            query = select(Route).where(Route.id == id)
            result = await session.execute(query)
            route = result.scalar_one_or_none()
            if not route:
                raise RouteNotFoundException(id)

            points_str = json.loads(route.points)
            coordinate_strings = points_str.split("], [")
            points = [
                list(coord.replace("[", "").replace("]", "").split(", "))
                for coord in coordinate_strings
            ]
            features = [
                FeatureModel(geometry=PointModel(coordinates=[float(lon), float(lat)]))
                for lon, lat, _, _ in points
            ]

            return FeatureCollectionModel(features=features)
