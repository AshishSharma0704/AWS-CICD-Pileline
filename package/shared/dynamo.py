import boto3

dynamodb = boto3.resource("dynamodb")


def get_table(table_name):
    return dynamodb.Table(table_name)


def put_item(table, item):

    table.put_item(
        Item=item
    )


def batch_write(table, items):

    with table.batch_writer() as batch:

        for item in items:

            batch.put_item(
                Item=item
            )


def delete_item(table, key):

    table.delete_item(
        Key=key
    )
    