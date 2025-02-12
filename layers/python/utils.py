import boto3
from uuid import uuid4

# Initialize DynamoDB Resource (Shared Across Functions)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")


def create_todo(task):
    todo_id = str(uuid4())
    item = {
        "id": todo_id,
        "task": task,
        "completed": False
    }
    table.put_item(Item=item)
    return item


def get_todo(todo_id):
    result = table.get_item(Key={"id": todo_id})
    return result.get("Item", None)


def get_all_todos():
    result = table.scan()
    return result["Items"]


def update_todo(todo_id, task, completed):
    result = table.update_item(
        Key={"id": todo_id},
        UpdateExpression="set task=:t, completed=:c",
        ExpressionAttributeValues={
            ":t": task,
            ":c": completed
        },
        ReturnValues="UPDATED_NEW"
    )
    return result["Attributes"]


def delete_todo(todo_id):
    table.delete_item(Key={"id": todo_id})
    return True
