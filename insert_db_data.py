import csv
import json
import sqlite3

connection = sqlite3.connect("db/sea_routes.db")
cursor = connection.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER,
    from_port TEXT,
    to_port TEXT,
    leg_duration INTEGER,
    points TEXT
)
"""
)

csv.field_size_limit(10**8)

with open("web_challenge.csv", "r") as file:
    reader = csv.reader(file)
    for i, vals in enumerate(reader):
        if i == 0:
            continue

        id = vals[0]
        from_port = vals[1]
        to_port = vals[2]
        leg_duration = vals[3]
        points = json.dumps(vals[4])
        cursor.execute(
            "INSERT INTO routes VALUES (?, ?, ?, ?, ?)",
            (
                id,
                from_port,
                to_port,
                leg_duration,
                points,
            ),
        )
    connection.commit()

print("Database data created!")

connection.close()
