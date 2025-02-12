import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")

def get_todo(event, context):
    todo_id = event["pathParameters"]["id"]
    result = table.get_item(Key={"id": todo_id})
    if "Item" in result:
        response = {
            "statusCode": 200,
            "body": json.dumps(result["Item"])
        }
    else:
        response = {
            "statusCode": 404,
            "body": json.dumps({"error": "TODO item not found"})
        }
    return response