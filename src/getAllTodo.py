import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")


def get_all_todo(event, context):
    response = table.scan()  # Fetch all items

    return {
        "statusCode": 200,
        "body": json.dumps(response["Items"])
    }
