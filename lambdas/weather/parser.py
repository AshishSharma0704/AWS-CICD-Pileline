from decimal import Decimal
from datetime import datetime, timezone


def parse(data):

    current = data["current"]

    return {
        "city": "Delhi",
        "temperature": Decimal(str(current["temperature_2m"])),
        "humidity": Decimal(str(current["relative_humidity_2m"])),
        "wind_speed": Decimal(str(current["wind_speed_10m"])),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
