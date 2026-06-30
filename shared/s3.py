import json
import boto3

s3 = boto3.client("s3")


def upload_json(bucket, key, data):
    """
    Upload JSON object to S3.
    """

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data)
    )


def download_json(bucket, key):
    """
    Download JSON from S3.
    """

    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    return json.loads(
        response["Body"].read()
    )


def upload_file(bucket, key, file_path):
    """
    Upload local file.
    """

    s3.upload_file(
        file_path,
        bucket,
        key
    )


def list_files(bucket, prefix=""):

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    return response.get("Contents", [])