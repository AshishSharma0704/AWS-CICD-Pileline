"""Pure transformation logic — unit-testable without AWS."""

def clean_email(email: str) -> str:
    return email.strip().lower()

def row_to_item(row: dict, source_key: str) -> dict:
    print("ROW KEYS:", list(row.keys()))

    customer_id = (
        row.get("customer_id")
        or row.get("\ufeffcustomer_id")
    )

    return {
        "customer_id": customer_id,
        "name": row["name"].strip(),
        "email": clean_email(row["email"]),
        "city": row["city"].strip(),
        "source_key": source_key,
    }