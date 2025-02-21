import json
import boto3
from uuid import uuid4

# Initialize DynamoDB Resource (Shared Across Functions)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodosNew")
api_gateway = boto3.client("apigatewaymanagementapi")


def create_todo(task):
    todo_id = str(uuid4())
    item = {
        "id": todo_id,
        "task": task,
        "completed": False
    }
    table.put_item(Item=item)

    # Notify all websocket clients
    connections_table = dynamodb.Table("TodoWebSocket")
    connections = connections_table.scan()["Items"]
    for connection in connections:
        api_gateway.post_to_connection(
            ConnectionId=connection["connectionId"],
            Data=json.dumps({"message": "New Todo Created", "todo": item})
        )

    response = {
        "statusCode": 200,
        "body": json.dumps({"message": "Todo created", "todo": item})
    }

    return response


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

    # Notify all websocket
    connections_table = dynamodb.Table("TodoWebSocket")
    connections = connections_table.scan()["Items"]
    for connection in connections:
        api_gateway.post_to_connection(
            ConnectionId=connection["connectionId"],
            Data = json.dumps({"message": "Todo Updated", "todo": result["Attributes"]})
        )

    response = {
        "statusCode": 200,
        "body": json.dumps(result["Attributes"])
    }

    return response


def delete_todo(todo_id):
    table.delete_item(Key={"id": todo_id})
    return True


def dynamo_db_stream(event):
    for record in event["Records"]:
        event_name = record["eventName"]  # INSERT, MODIFY, REMOVE
        new_image = record.get("dynamodb", {}).get("NewImage", {})
        old_image = record.get("dynamodb", {}).get("OldImage", {})

        if event_name == "INSERT":
            print(f"New item added: {json.dumps(new_image)}")
        elif event_name == "MODIFY":
            print(f"Item updated: Old: {json.dumps(old_image)}, New: {json.dumps(new_image)}")
        elif event_name == "REMOVE":
            print(f"Item deleted: {json.dumps(old_image)}")

    return {
        "statusCode": 200,
        "body": "Processed Successfully"
    }
