import json
import os
from datetime import datetime, timezone
from urllib.request import urlopen

from shared.config import (
    RAW_BUCKET as CONFIG_RAW_BUCKET,
    API_URLS,
    PREFIXES,
    TABLES,
)
from shared.s3 import upload_json
from shared.dynamo import get_table, batch_write
from shared.validators import validate_transit
from shared.logger import info
from parser import parse

RAW_BUCKET = os.environ.get("RAW_BUCKET", CONFIG_RAW_BUCKET)
TABLE_NAME = os.environ.get("TABLE_NAME", TABLES["transit"])


def lambda_handler(event, context):
    info("Fetching transit data...")

    response = urlopen(API_URLS["transit"])
    data = json.loads(response.read().decode("utf-8"))

    if not validate_transit(data):
        raise Exception("Invalid transit response")

    file_name = (
        PREFIXES["transit"]
        + f"transit_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )

    upload_json(bucket=RAW_BUCKET, key=file_name, data=data)
    info(f"Raw transit data uploaded to s3://{RAW_BUCKET}/{file_name}")

    items = [parse(route) for route in data.get("data", [])]
    table = get_table(TABLE_NAME)
    batch_write(table=table, items=items)

    info(f"{len(items)} transit records loaded into {TABLE_NAME}")

    return {
        "statusCode": 200,
        "records_loaded": len(items),
        "bucket": RAW_BUCKET,
        "s3_key": file_name,
        "table": TABLE_NAME,
    }
