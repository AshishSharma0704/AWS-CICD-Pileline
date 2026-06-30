import json
from urllib.request import urlopen
from datetime import datetime, timezone

from shared.config import (
    RAW_BUCKET,
    EARTHQUAKE_API,
    EARTHQUAKE_PREFIX,
    EARTHQUAKE_TABLE,
)

from shared.s3 import upload_json
from shared.dynamo import get_table, batch_write
from shared.validators import validate_earthquake
from shared.logger import info
from parser import parse


def lambda_handler(event, context):

    info("Fetching earthquake data...")

    response = urlopen(EARTHQUAKE_API)

    data = json.loads(
        response.read().decode("utf-8")
    )

    file_name = (
        EARTHQUAKE_PREFIX
        + f"earthquake_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )

    upload_json(
        RAW_BUCKET,
        file_name,
        data
    )

    info("Raw JSON uploaded to S3")

    items = []

    for feature in data.get("features", []):

        if not validate_earthquake(feature):
            continue

        items.append(parse(feature))

    table = get_table(EARTHQUAKE_TABLE)

    batch_write(
        table,
        items
    )

    info(f"{len(items)} records loaded")

    return {
        "statusCode": 200,
        "records_loaded": len(items),
        "s3_file": file_name
    }
