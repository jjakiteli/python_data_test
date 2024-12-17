from pydantic import BaseModel
from sqlalchemy import Float, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class RouteModel(BaseModel):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int


class Base(DeclarativeBase):
    pass


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    from_port: Mapped[str] = mapped_column(Text)
    to_port: Mapped[str] = mapped_column(Text)
    leg_duration: Mapped[float] = mapped_column(Float)
    points: Mapped[str] = mapped_column(Text)
