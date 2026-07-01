from decimal import Decimal


def parse(product):
    return {
        "product_id": str(product.get("id", "")),
        "title": product.get("title", ""),
        "price": Decimal(str(product.get("price", 0))) if product.get("price") is not None else Decimal("0"),
        "description": product.get("description", ""),
        "category": product.get("category", ""),
        "image": product.get("image", ""),
        "rating": Decimal(str(product.get("rating", {}).get("rate", 0))) if isinstance(product.get("rating"), dict) else Decimal("0"),
    }
