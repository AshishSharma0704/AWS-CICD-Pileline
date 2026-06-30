from decimal import Decimal
from datetime import datetime, timezone


def parse(feature):
    """
    Convert a USGS earthquake feature into a DynamoDB item.
    """

    mag = feature["properties"]["mag"]

    coords = feature["geometry"]["coordinates"]

    if mag < 4:
        severity = "Low"
    elif mag < 6:
        severity = "Moderate"
    else:
        severity = "High"

    return {
        "event_id": feature["id"],
        "magnitude": Decimal(str(mag)),
        "place": feature["properties"]["place"],
        "latitude": Decimal(str(coords[1])),
        "longitude": Decimal(str(coords[0])),
        "depth": Decimal(str(coords[2])),
        "event_time": datetime.fromtimestamp(
            feature["properties"]["time"] / 1000,
            tz=timezone.utc
        ).isoformat(),
        "severity": severity,
        "ingestion_date": datetime.now(
            timezone.utc
        ).date().isoformat()
    }