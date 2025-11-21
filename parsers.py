"""
Parsing utilities for GPS data files used by the Location Privacy Risk Analyzer.

YOU WANT: STRAVA‑STYLE JSON ONLY (NO GPX FOR NOW)
-------------------------------------------------
Your goal here is:
  - Take a JSON export that looks like Strava data.
  - Pull out the route points and times.
  - Convert them into a simple, consistent list/array of points:
        [
            {"lat": <float>, "lon": <float>, "timestamp": <datetime or string>},
            ...
        ]

Below is a step‑by‑step guide for what to implement (conceptual only, no code).

1. Decide the internal format you will return
   - Pick ONE structure you will use everywhere in the app, e.g.:
       * A Python list where each element is a dict with keys:
         "lat", "lon", "timestamp"
       * OR a pandas DataFrame with columns "lat", "lon", "timestamp".
   - Stick to that format so `analysis.py` can rely on it.

2. Understand the Strava JSON you want to support
   - Open a real Strava JSON file in a text editor and inspect its structure.
   - Find where the per‑point data lives. Common patterns:
       * A "streams" structure with separate arrays:
           - One array for positions (e.g., list of [lat, lon] pairs).
           - One array for time (e.g., seconds since the start of the activity).
       * Or a direct list of data points where each object already has "lat", "lng", "time".
   - Write down (for yourself) the exact keys you will rely on, e.g.:
       * positions key name
       * time key name
       * activity start time field (used to convert "seconds since start" into real timestamps)

3. Implement `parse_strava_json(path_or_file)` (name is up to you)
   - Step A: Load the JSON from disk or file‑like object.
   - Step B: Navigate to the part containing the streams / points.
       * Access the positions array (e.g., list of [lat, lon] pairs).
       * Access the time array (e.g., list of seconds since start, or absolute timestamps).
   - Step C: Handle timestamps
       * If the time values are "seconds since start":
           - Get the activity start time from the JSON (usually a field like "start_date" or similar).
           - Convert each "seconds since start" value into a real timestamp by adding it to start time.
       * If the time values are already absolute timestamps:
           - Convert them into a consistent type (e.g., Python datetime or ISO string).
   - Step D: Build your normalized list
       * For each index i:
           - Extract lat and lon from the positions data.
           - Extract the corresponding time value.
           - Create your normalized point: {"lat": ..., "lon": ..., "timestamp": ...}
       * Collect all points into a list (or DataFrame).
   - Step E: Handle edge cases
       * If positions and time arrays have different lengths, decide how to handle it
         (e.g., truncate to the shorter length).
       * If some points are clearly invalid (lat or lon missing or out of range), skip them.

4. Implement a general entry function (e.g., `parse_gps_file(filename)` or `parse_json_file(filename)`)
   - This is the function that `app.py` will call.
   - What it should do:
       * Confirm that the file extension is `.json` (since you are focusing on JSON only).
       * Open the file and call `parse_strava_json(...)`.
       * Optionally enforce basic sanity checks:
           - Require at least a minimum number of points (e.g., > 10).
           - Raise a clear exception or error message if parsing fails.

5. (Optional) Helper to convert to pandas
   - If you prefer using pandas in `analysis.py`:
       * Write a helper that takes your list of dicts and returns a DataFrame with
         columns "lat", "lon", "timestamp".
       * Make sure the timestamp column is a proper datetime type if you want to use time‑based operations.
"""
#JSON means JavaScript Object Notation 

import json 

with open('sample_data/sample_activity.json') as file :
    data = json.load(file) #.loads is for a variable/string, load is for a file object parsing | it just storesthe data in the var 
    # print(data) # data is a dictionary type currently 
    streams = data['streams'] # streams is currently a string, so we cant just do data['latlng']
    latlng = streams['latlng']
    distance = streams['distance']

points = []

for i in range(len(latlng)): 

    lat = latlng[i][0]
    lon = latlng[i][1]

    
    point = {
        "lat": lat,
        "lon":  lon,
        "timestamp": f"2025-01-01T07:30:{distance[i]}Z"
    }

    points.append(point)

print(points)
   

        



