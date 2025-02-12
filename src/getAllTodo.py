import json
from layers.python.utils import get_all_todos


def lambda_handler(event, context):
    todos = get_all_todos()
    return {"statusCode": 200, "body": json.dumps(todos)}
