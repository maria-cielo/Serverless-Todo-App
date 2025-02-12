import json
from layers.python.utils import create_todo

def lambda_handler(event, context):
    data = json.loads(event["body"])
    todo = create_todo(data["task"])
    return {
        "statusCode": 201,
        "body": json.dumps({"message": "Todo created", "todo": todo})
    }
