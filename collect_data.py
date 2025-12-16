from datetime import datetime, timezone, timedelta
import requests
import csv
import os
import sys

# =========================
# WIB TIME WINDOW (06–10)
# =========================
# WIB = timezone(timedelta(hours=7))

# now_utc = datetime.now(timezone.utc)
# now_wib = now_utc.astimezone(WIB)

# if not (6 <= now_wib.hour < 10):
#     print(f"Skipping run: outside WIB window ({now_wib.isoformat()})")
#     sys.exit(0)

# =========================
# ENV & COORDINATES
# =========================
ORS_API_KEY = os.getenv("ORS_API_KEY")
if not ORS_API_KEY:
    print("ORS_API_KEY not found")
    sys.exit(0)   # do NOT fail GitHub Actions

# ORS format: longitude,latitude
PASKAL = "107.5923271,-6.9157482"
TKI = "107.5580945,-6.958391"

url = "https://api.openrouteservice.org/v2/directions/driving-car"

params = {
    "api_key": ORS_API_KEY,
    "start": PASKAL,
    "end": TKI
}

headers = {
    "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
    "User-Agent": "TravelTimeResearch/1.0 (academic use)"
}

# =========================
# API CALL
# =========================
response = requests.get(url, params=params, headers=headers)

if response.status_code != 200:
    print("ORS request failed")
    print("Status:", response.status_code)
    print("Response:", response.text)
    sys.exit(0)   # keep workflow GREEN

data = response.json()

# =========================
# PARSE RESPONSE
# =========================
summary = data["features"][0]["properties"]["summary"]
duration = summary["duration"]   # seconds
distance = summary["distance"]   # meters

timestamp = datetime.now(timezone.utc).isoformat()

# =========================
# SAVE CSV
# =========================
os.makedirs("data", exist_ok=True)
file_path = "data/bandung_route.csv"
file_exists = os.path.isfile(file_path)

with open(file_path, "a", newline="") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["timestamp_utc", "duration_sec", "distance_m"])
    writer.writerow([timestamp, duration, distance])

print("Logged:", timestamp, duration, distance)
