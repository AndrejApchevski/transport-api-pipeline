import os
import requests
import psycopg2
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
ATCO_CODE = "490008660N"

# Build API request
url = f"https://transportapi.com/v3/uk/bus/stop/{ATCO_CODE}/live.json"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "group": "route",
    "limit": 5,
    "nextbuses": "yes"
}

# Call API
response = requests.get(url, params=params)
data = response.json()

# Connect to DB
conn = psycopg2.connect(
    host="localhost",
    database="transport_data",
    user="postgres",
    password="your_password_here"
)
cur = conn.cursor()

# Insert data into table
for service in data.get("departures", {}).get("all", []):
    line = service.get("line")
    direction = service.get("direction")
    aimed = service.get("aimed_departure_time")
    expected = service.get("expected_departure_time")
    operator = service.get("operator_name")
    stop_name = data.get("stop_name")

    cur.execute("""
        INSERT INTO bus_live_data (line_name, direction, aimed_departure, expected_departure, operator_name, stop_name, atcocode)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (line, direction, aimed, expected, operator, stop_name, ATCO_CODE))

conn.commit()
cur.close()
conn.close()

print("✅ Data inserted successfully.")
