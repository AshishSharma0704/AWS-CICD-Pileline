import json
from decimal import Decimal
from datetime import datetime, timezone
from urllib.request import urlopen

from shared.config import RAW_BUCKET, PREFIXES, TABLES, API_URLS
from shared.s3 import s3
from shared.dynamo import dynamodb

table = dynamodb.Table(TABLES["weather"])


def lambda_handler(event, context):

    # Fetch weather data
    response = urlopen(API_URLS["weather"])
    data = json.loads(response.read().decode("utf-8"))

    # Save raw JSON to S3
    file_name = (
        f"{PREFIXES['weather']}"
        f"weather_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )

    s3.put_object(
        Bucket=RAW_BUCKET,
        Key=file_name,
        Body=json.dumps(data)
    )

    current = data["current"]

    item = {
        "city": "Delhi",
        "temperature": Decimal(str(current["temperature_2m"])),
        "humidity": Decimal(str(current["relative_humidity_2m"])),
        "wind_speed": Decimal(str(current["wind_speed_10m"])),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "message": "Weather ETL completed",
        "s3_key": file_name
    }
