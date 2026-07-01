def validate_earthquake(feature):
    """
    Validate an earthquake record before parsing.
    """

    if feature is None:
        return False

    if "properties" not in feature:
        return False

    if "geometry" not in feature:
        return False

    if feature["properties"].get("mag") is None:
        return False

    if feature["geometry"].get("coordinates") is None:
        return False

    if len(feature["geometry"]["coordinates"]) != 3:
        return False

    return True


def validate_weather(data):
    """
    Validate weather API response.
    """

    if data is None:
        return False

    if "current" not in data:
        return False

    current = data["current"]

    required_fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
    ]

    for field in required_fields:
        if field not in current:
            return False

    return True


def validate_product(data):
    if data is None or not isinstance(data, list):
        return False

    for item in data:
        if not isinstance(item, dict):
            return False
        if item.get("id") is None:
            return False

    return True


def validate_transit(data):
    if data is None or not isinstance(data, dict):
        return False

    if "data" not in data or not isinstance(data["data"], list):
        return False

    return True
