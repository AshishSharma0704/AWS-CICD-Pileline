"""
Central configuration for the ETL Platform.
Every Lambda imports values from here.
"""

# ==========================
# S3
# ==========================

RAW_BUCKET = "multi-source-raw-data"

PREFIXES = {
    "earthquake": "earthquake/",
    "weather": "weather/",
    "product": "product/",
    "transit": "transit/",
}


# ==========================
# DynamoDB Tables
# ==========================

TABLES = {
    "earthquake": "EarthquakeEvents",
    "weather": "WeatherReadings",
    "product": "Products",
    "transit": "TransitData",
}


# ==========================
# API URLs
# ==========================

# ==========================
# API URLs
# ==========================

API_URLS = {

    "earthquake": (
        "https://earthquake.usgs.gov/fdsnws/event/1/query?"
        "format=geojson"
        "&starttime=2026-05-01"
        "&endtime=2026-05-27"
        "&minmagnitude=2.5"
        "&orderby=time"
    ),

    "weather": (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=28.6139"
        "&longitude=77.2090"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    ),

    "product": (
        "https://fakestoreapi.com/products"
    ),

    "transit": (
        "https://api-v3.mbta.com/routes"
    )
}
