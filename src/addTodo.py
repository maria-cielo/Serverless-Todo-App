import json
import boto3
from uuid import uuid4

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")

def add_todo(event, context):
    data = json.loads(event["body"]) # receive event body
    todo_id = str(uuid4())
    item = {
        "id": todo_id,
        "task": data["task"],
        "completed": False
    }
    table.put_item(Item=item)
    response = {
        "statusCode": 201,
        "body": json.dumps({"message": "Todo created", "todo": item})
    }
    return response
