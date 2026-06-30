"""
Validation functions for every data source.
"""


def validate_earthquake(feature):

    if feature is None:
        return False

    if feature.get("properties") is None:
        return False

    if feature["properties"].get("mag") is None:
        return False

    if feature.get("geometry") is None:
        return False

    return True


def validate_weather(record):
    return True


def validate_product(record):
    return True


def validate_transit(record):
    return True