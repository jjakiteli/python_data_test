import json
import sqlite3
from typing import Optional

from pydantic_geojson import FeatureCollectionModel, FeatureModel, PointModel

from models import RouteModel


class SqliteRepository:
    def get_all_routes(self) -> list[RouteModel]:
        connection = sqlite3.connect("db/sea_routes.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, from_port, to_port, leg_duration FROM routes
            """
        )
        values = cursor.fetchall()
        return_list = []
        for val in values:
            return_list.append(
                RouteModel(
                    route_id=val[0],
                    from_port=val[1],
                    to_port=val[2],
                    leg_duration=val[3],
                )
            )

        cursor.close()
        connection.close()
        return return_list

    def get_route(self, id: int) -> Optional[FeatureCollectionModel]:
        connection = sqlite3.connect("db/sea_routes.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT points FROM routes WHERE id == ?
            """,
            (id,),
        )
        values = cursor.fetchone()
        if values is None:
            return None

        points_str = json.loads(values[0])
        coordinate_strings = points_str.split("], [")
        points = [
            list(coord.replace("[", "").replace("]", "").split(", "))
            for coord in coordinate_strings
        ]
        features = [
            FeatureModel(geometry=PointModel(coordinates=[float(lon), float(lat)]))
            for lon, lat, _, _ in points
        ]

        geojson = FeatureCollectionModel(features=features)
        cursor.close()
        connection.close()
        return geojson
