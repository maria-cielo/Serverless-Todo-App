import json
from layers.python.utils import (
    create_todo,
    dynamo_db_stream,
)


def lambda_handler(event, context):
    print("Received event: ", event)

    if "Records" in event:
        return dynamo_db_stream(event)

    data = json.loads(event.get("body", {}))
    task = data.get("task")
    completed = data.get("completed", "false")

    todo = create_todo(task, completed)

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Todo created", "todo": todo})
    }
