import os
import requests
import psycopg2
import json
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")
ATCO_CODE = "490000235Z"  # Stop: New Oxford Street (Stop Z)

# Build API request
url = f"https://transportapi.com/v3/uk/bus/stop/{ATCO_CODE}/live.json"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "group": "route",  # Grouped by bus line (e.g., "188", "98")
    "limit": 5,
    "nextbuses": "yes"
}

# Call the API
response = requests.get(url, params=params)
print("🔗 Request URL:", response.url)

if response.status_code != 200:
    print("❌ API request failed:", response.status_code)
    print(response.text)
    exit()

data = response.json()

# Print the grouped line codes to confirm structure
print("🚌 Grouped by line:", list(data.get("departures", {}).keys()))

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="transport_data",
        user="postgres",
        password="1000lordofrings"
    )
    cur = conn.cursor()
except Exception as e:
    print("❌ Failed to connect to database:", e)
    exit()

stop_name = data.get("stop_name", "Unknown")

# Loop through each line group
departures_by_line = data.get("departures", {})
insert_count = 0

for line_code, departures in departures_by_line.items():
    for service in departures:
        line = service.get("line")
        direction = service.get("direction")
        aimed = service.get("aimed_departure_time")
        expected = service.get("expected_departure_time")
        operator = service.get("operator_name")

        print(f"🚍 Inserting: {line}, {direction}, {aimed}, {expected}, {operator}, {stop_name}")

        try:
            cur.execute("""
                INSERT INTO bus_live_data (
                    line_name, direction, aimed_departure,
                    expected_departure, operator_name, stop_name, atcocode
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (line, direction, aimed, expected, operator, stop_name, ATCO_CODE))
            insert_count += 1
        except Exception as e:
            print("❌ Insert error:", e)
            continue

# Finalize DB transaction
conn.commit()
cur.close()
conn.close()

print(f"✅ {insert_count} rows inserted into PostgreSQL.")
