import json
import boto3
from layers.python.utils import get_todo

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")


def lambda_handler(event, context):
    todo_id = event["pathParameters"]["id"]
    todo = get_todo(todo_id)
    if todo:
        return {"statusCode": 200, "body": json.dumps(todo)}
    return {"statusCode": 404, "body": json.dumps({"error": "TODO item not found"})}
