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
from shared.validators import validate_product
from shared.logger import info
from parser import parse

RAW_BUCKET = os.environ.get("RAW_BUCKET", CONFIG_RAW_BUCKET)
TABLE_NAME = os.environ.get("TABLE_NAME", TABLES["product"])


def lambda_handler(event, context):
    info("Fetching product data...")

    response = urlopen(API_URLS["product"])
    data = json.loads(response.read().decode("utf-8"))

    if not validate_product(data):
        raise Exception("Invalid product response")

    file_name = (
        PREFIXES["product"]
        + f"product_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )

    upload_json(bucket=RAW_BUCKET, key=file_name, data=data)
    info(f"Raw product data uploaded to s3://{RAW_BUCKET}/{file_name}")

    items = [parse(item) for item in data]
    table = get_table(TABLE_NAME)
    batch_write(table=table, items=items)

    info(f"{len(items)} product records loaded into {TABLE_NAME}")

    return {
        "statusCode": 200,
        "records_loaded": len(items),
        "bucket": RAW_BUCKET,
        "s3_key": file_name,
        "table": TABLE_NAME,
    }
