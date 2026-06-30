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
