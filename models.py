from pydantic import BaseModel


class RouteModel(BaseModel):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int
