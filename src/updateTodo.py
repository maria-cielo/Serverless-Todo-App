import json
from layers.python.utils import update_todo


def lambda_handler(event, context):
    todo_id = event["pathParameters"]["id"]
    data = json.loads(event["body"])
    updated_todo = update_todo(todo_id, data["task"], data["completed"])
    return {"statusCode": 200, "body": json.dumps(updated_todo)}
