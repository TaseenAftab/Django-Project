# FuelTracker Pro: Optimal Routing & Cost Minimizer

FuelTracker is an enterprise-grade Django REST API built to calculate the most cost-effective cross-country driving routes. Instead of just finding the shortest distance between two points, FuelTracker uses a highly optimized Dijkstra's algorithm to calculate exactly where a driver should stop for gas to **mathematically minimize the total dollar amount spent on fuel** along the trip.

## 🚀 What This Project Achieves

This project solves the complex constraints of long-haul logistics:
1. **Dynamic Cost Optimization**: It factors in a vehicle's maximum range (500 miles) and consumption (10 MPG) to hunt down the absolute cheapest retail fuel prices along the route. 
2. **Lightning Fast Spatial Queries**: It loads tens of thousands of gas stations into an in-memory `scipy` KD-Tree to perform blazing-fast coordinate geometry lookups.
3. **Optimized API Payload**: Instead of hammering third-party mapping APIs, it makes exactly **1 single API call** to OpenRouteService to fetch the entire master route, and then uses pure mathematics (Shapely) to perfectly slice that geometry into a segmented GeoJSON response.

---

## 🛠️ Local Setup Instructions

Follow these steps to run the routing API locally on your machine.

### 1. Prerequisites
- Python 3.10+
- Django 5.x
- `pip` for dependency management

### 2. Installation
Clone the repository and install the required dependencies (like `django`, `djangorestframework`, `shapely`, `scipy`, `requests`, etc.):
```bash
# Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies (assuming a requirements.txt exists)
pip install -r requirements.txt
```

### 3. OpenRouteService API Key (Optional)
The routing engine relies on the OpenRouteService API. The project has a built-in default testing key, but for heavy usage, you should optionally provide your own API key.
1. Create a `.env` file in the root directory.
2. Add your key:
```env
ORS_API_KEY=your_personal_api_key_here
```

### 4. Run the Server
Because the SQLite database is pre-loaded with the truck stop data, you can immediately start the server:
```bash
python manage.py runserver
```

---

## 📡 How to Use the API

The primary endpoint is a `POST` request to calculate the route.

**Endpoint:** `http://127.0.0.1:8000/api/`  
**Method:** `POST`  
**Content-Type:** `application/json`

### Request Payload
Send the `start` and `end` coordinates in `[latitude, longitude]` format.
```json
{
    "start": [36.705289, -118.882689],
    "end": [27.7567667, -81.4639835]
}
```

---

## 🧠 Interpreting the Response

If successful, the API returns a massive payload specifically structured for instant Frontend map rendering.

```json
{
  "geojson": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "segment_index": 1,
          "length_miles": 415.31
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [ ... ]
        }
      }
    ]
  },
  "total_fuel_cost": 668.19,
  "stops": [
    {
      "name": "CEFCO #1086",
      "address": "100 EAST TEXAS ST",
      "city": "Longview",
      "state": "TX",
      "retail_price": 2.96,
      "coordinates": [-94.708863, 32.451767],
      "proj_dist": 1698.34
    }
  ]
}
```

### 1. The `geojson` Object
This is a standard GeoJSON `FeatureCollection`. It contains multiple `LineString` features representing the exact route segments between each required gas station stop. Your frontend developer can drop this directly into **Mapbox** or **Leaflet** to instantly draw the entire cross-country route with different colored segments.

### 2. The `total_fuel_cost` Float
This is the optimized grand total (in USD) spent on gas for the entire trip, calculated using the specific retail prices at the selected stops.

### 3. The `stops` Array
This provides the detailed metadata for every single gas station the algorithm selected. The frontend can iterate through this array to place interactive pins/markers over the GeoJSON route, displaying the Truck Stop Name, City, and the exact price they paid for fuel at that specific location.
