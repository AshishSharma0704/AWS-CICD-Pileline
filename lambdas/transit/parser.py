from decimal import Decimal


def parse(route):
    attributes = route.get("attributes", {})
    return {
        "route_id": route.get("id", ""),
        "short_name": attributes.get("short_name", ""),
        "long_name": attributes.get("long_name", ""),
        "route_type": str(attributes.get("route_type", "")),
        "description": attributes.get("description", ""),
        "color": attributes.get("color", ""),
        "text_color": attributes.get("text_color", ""),
    }
