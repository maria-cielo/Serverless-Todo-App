from layers.python.utils import delete_todo

def lambda_handler(event, context):
    todo_id = event["pathParameters"]["id"]
    delete_todo(todo_id)
    return {"statusCode": 204}
