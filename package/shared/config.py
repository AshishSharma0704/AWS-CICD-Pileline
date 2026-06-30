"""
Central configuration for the ETL Platform.
Every Lambda imports values from here.
"""

# ==========================
# S3
# ==========================

RAW_BUCKET = "raw-data-platform"

EARTHQUAKE_PREFIX = "earthquake/"
WEATHER_PREFIX = "weather/"
PRODUCT_PREFIX = "products/"
TRANSIT_PREFIX = "transit/"


# ==========================
# DynamoDB Tables
# ==========================

EARTHQUAKE_TABLE = "EarthquakeEvents"

WEATHER_TABLE = "WeatherMetrics"

PRODUCT_TABLE = "ProductCatalog"

TRANSIT_TABLE = "TransitRecords"


# ==========================
# API URLs
# ==========================

EARTHQUAKE_API = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?"
    "format=geojson"
    "&starttime=2026-05-01"
    "&endtime=2026-05-27"
    "&minmagnitude=2.5"
    "&orderby=time"
)

# Placeholder APIs (we'll update later)

WEATHER_API = ""

PRODUCT_API = ""

TRANSIT_API = ""