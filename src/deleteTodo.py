import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")

def delete(event, context):
    todo_id = event["pathParameters"]["id"]
    table.delete_item(Key={"id": todo_id})
    response = {
        "statusCode": 204,
    }
    return response
