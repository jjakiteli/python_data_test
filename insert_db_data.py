import pandas as pd
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker


def insert_data():
    DATABASE_URL = "sqlite:///db/sea_routes.db"
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    session_factory = SessionLocal()

    routes_table = Table("sea_routes", metadata, autoload_with=engine)

    csv_data = pd.read_csv("web_challenge.csv")

    current_entries = session_factory.query(routes_table).all()
    route_ids = {route.route_id for route in current_entries}

    new_data = csv_data[~csv_data["route_id"].isin(route_ids)]

    if not new_data.empty:
        new_data.to_sql("sea_routes", con=engine, if_exists="append", index=False)
        print(f"{len(new_data)} new records added.")
    else:
        print("No new records to add.")
