import json
from layers.python.utils import (
    update_todo,
    dynamo_db_stream,
)


def lambda_handler(event, context):
    if "Records" in event:
        return dynamo_db_stream(event)
    todo_id = event["pathParameters"]["id"]
    data = json.loads(event.get("body", {}))
    updated_todo = update_todo(todo_id, data["task"], data["completed"])
    return {"statusCode": 200, "body": json.dumps(updated_todo)}
