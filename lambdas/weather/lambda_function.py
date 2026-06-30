import json
from urllib.request import urlopen
from datetime import datetime, timezone

from shared.config import (
    RAW_BUCKET,
    API_URLS,
    PREFIXES,
    TABLES,
)
from shared.s3 import upload_json
from shared.dynamo import get_table, batch_write
from shared.validators import validate_weather
from shared.logger import info
from parser import parse


def lambda_handler(event, context):

    info("Fetching weather data...")

    # Fetch Weather API
    response = urlopen(API_URLS["weather"])

    data = json.loads(
        response.read().decode("utf-8")
    )

    # Validate response
    if not validate_weather(data):
        raise Exception("Invalid weather response")

    # Save raw JSON to S3
    file_name = (
        PREFIXES["weather"]
        + f"weather_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )

    upload_json(
        bucket=RAW_BUCKET,
        key=file_name,
        data=data
    )

    info(f"Raw weather data uploaded to s3://{RAW_BUCKET}/{file_name}")

    # Transform
    item = parse(data)

    # Load into DynamoDB
    table = get_table(TABLES["weather"])

    batch_write(
        table=table,
        items=[item]
    )

    info(f"Weather data loaded into {TABLES['weather']}")

    return {
        "statusCode": 200,
        "records_loaded": 1,
        "bucket": RAW_BUCKET,
        "s3_key": file_name,
        "table": TABLES["weather"],
    }
