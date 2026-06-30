import json
from datetime import datetime, timezone
from urllib.request import urlopen

from shared.config import (
    RAW_BUCKET,
    API_URLS,
    PREFIXES,
    TABLES,
)
from shared.s3 import upload_json
from shared.dynamo import get_table, batch_write
from shared.validators import validate_earthquake
from shared.logger import info
from parser import parse


def lambda_handler(event, context):

    info("Fetching earthquake data...")

    # Fetch data from API
    response = urlopen(API_URLS["earthquake"])

    data = json.loads(
        response.read().decode("utf-8")
    )

    # Create S3 object key
    file_name = (
        PREFIXES["earthquake"]
        + f"earthquake_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )

    # Upload raw JSON to S3
    upload_json(
        bucket=RAW_BUCKET,
        key=file_name,
        data=data
    )

    info(f"Raw data uploaded to s3://{RAW_BUCKET}/{file_name}")

    # Transform records
    items = []

    for feature in data.get("features", []):

        if not validate_earthquake(feature):
            continue

        items.append(parse(feature))

    # Load into DynamoDB
    table = get_table(TABLES["earthquake"])

    batch_write(
        table=table,
        items=items
    )

    info(f"{len(items)} records loaded into {TABLES['earthquake']}")

    return {
        "statusCode": 200,
        "records_loaded": len(items),
        "bucket": RAW_BUCKET,
        "s3_key": file_name,
        "table": TABLES["earthquake"],
    }
