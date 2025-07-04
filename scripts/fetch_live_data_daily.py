import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

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
    "group": "route",
    "limit": 100,  # Daily mode
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
departures_by_line = data.get("departures", {})
print("🚌 Grouped by line:", list(departures_by_line.keys()))
print(f"📊 Total lines fetched: {len(departures_by_line)}")
for line_code, departures in departures_by_line.items():
    print(f"   🚌 Line {line_code}: {len(departures)} departures")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host="localhost",
        database="transport_data",
        user="postgres",
        password="admin"
    )
    cur = conn.cursor()
except Exception as e:
    print("❌ Failed to connect to database:", e)
    exit()

# Metadata
stop_name = data.get("stop_name", "Unknown")
fetched_at = datetime.now()
insert_count = 0

# Insert into bus_live_data
for line_code, departures in departures_by_line.items():
    for service in departures:
        line = service.get("line")
        direction = service.get("direction")
        aimed = service.get("aimed_departure_time")
        expected = service.get("expected_departure_time")
        operator = service.get("operator_name")

        print(f"🚍 Inserting: {line}, {direction}, {aimed}, {expected}, {operator}, {stop_name}, {fetched_at}")

        try:
            cur.execute("""
                INSERT INTO bus_live_data (
                    line_name, direction, aimed_departure,
                    expected_departure, operator_name,
                    stop_name, atcocode, fetched_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                line, direction, aimed, expected,
                operator, stop_name, ATCO_CODE, fetched_at
            ))
            insert_count += 1
        except Exception as e:
            print("❌ Insert error:", e)
            continue

conn.commit()
cur.close()
conn.close()

print(f"✅ {insert_count} rows inserted into PostgreSQL at {fetched_at.strftime('%Y-%m-%d %H:%M:%S')}")
