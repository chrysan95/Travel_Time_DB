from datetime import datetime, timezone, timedelta

# Define WIB timezone
WIB = timezone(timedelta(hours=7))

now_utc = datetime.now(timezone.utc)
now_wib = now_utc.astimezone(WIB)

# Only allow 06:00–10:00 WIB
if not (6 <= now_wib.hour < 10):
    print(f"Skipping run: outside WIB window ({now_wib.isoformat()})")
    exit(0)

import requests
import csv
from datetime import datetime, timezone
import os

ORS_API_KEY = os.getenv("ORS_API_KEY")
if not ORS_API_KEY:
    raise RuntimeError("ORS_API_KEY not found")

# ORS format: [longitude, latitude]
PASKAL = [107.5923271, -6.9157482]
TKI = [107.5580945, -6.958391]

url = "https://api.openrouteservice.org/v2/directions/driving-car"

headers = {
    "Authorization": ORS_API_KEY,
    "Content-Type": "application/json"
}

body = {
    "coordinates": [PASKAL, TKI]
}

response = requests.post(url, json=body, headers=headers)
data = response.json()

if response.status_code != 200:
    print("Request failed")
    print("Status:", response.status_code)
    print("Response:", data)
    raise SystemExit

summary = data["routes"][0]["summary"]
duration = summary["duration"]
distance = summary["distance"]

# UTC timestamp
timestamp = datetime.now(timezone.utc).isoformat()

os.makedirs("data", exist_ok=True)
file_path = "data/bandung_route.csv"
file_exists = os.path.isfile(file_path)

with open(file_path, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["timestamp_utc", "duration_sec", "distance_m"])
    writer.writerow([timestamp, duration, distance])

print("Logged:", timestamp, duration)
