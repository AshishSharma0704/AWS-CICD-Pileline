"""
Central configuration for the ETL Platform.
Every Lambda imports values from here.
"""

# ==========================
# S3
# ==========================

RAW_BUCKET = "raw-data-platform"

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
    "weather": "WeatherMetrics",
    "product": "ProductCatalog",
    "transit": "TransitRecords",
}


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

    "weather": "",

    "product": "",

    "transit": "",
}
