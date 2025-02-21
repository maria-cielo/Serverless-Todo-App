from layers.python.utils import (
    delete_todo,
    dynamo_db_stream,
)


def lambda_handler(event, context):
    if "Records" in event:
        return dynamo_db_stream(event)
    todo_id = event["pathParameters"]["id"]
    delete_todo(todo_id)
    return {"statusCode": 204}
