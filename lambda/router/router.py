import json

def lambda_handler(event, context):
    print("Incoming Event:")
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps("Router Lambda Invoked Successfully")
    }