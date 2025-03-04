import json
import boto3
from uuid import uuid4


APIGW_MANAGEMENT_API = "https://vu7zzd52p2.execute-api.us-east-1.amazonaws.com/dev"
QUEUE_URL = f"https://sqs.us-east-1.amazonaws.com/598858048125/TodoQueue"

api_gateway = boto3.client("apigatewaymanagementapi",
                           endpoint_url=APIGW_MANAGEMENT_API
                           )
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodosNew")
sqs = boto3.client("sqs")


def create_todo(task, completed):
    todo_id = str(uuid4())
    item = {
        "id": todo_id,
        "task": task,
        "completed": completed
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
    update_expression_parts = []
    expression_values = {}

    if task is not None:
        update_expression_parts.append("task = :t")
        expression_values[":t"] = task

    if completed is not None:
        update_expression_parts.append("completed = :c")
        expression_values[":c"] = completed

    update_expression = "SET " + ", ".join(update_expression_parts)

    result = table.update_item(
        Key={"id": todo_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
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
        print("Received event: ", json.dumps(event, indent=2))

        message_body = {}

        if "eventName" in record:  # DynamoDB Stream Event
            event_name = record.get("eventName", "")  # INSERT, MODIFY, REMOVE
            new_image = record.get("dynamodb", {}).get("NewImage", {})

            message_body = {
                "id": new_image.get("id", {}).get("S"),
                "task": new_image.get("task", {}).get("S"),
                "completed": new_image.get("completed", {}).get("BOOL"),
                "eventType": event_name
            }
            print(f"DynamoDB Event: {event_name} -> {json.dumps(new_image)}")

        elif "body" in record:  # SQS Event
            try:
                body = json.loads(record["body"])  # Parse the string body to JSON
                event_type = body.get("eventType", "UNKNOWN")
                print(f"SQS Event: {event_type} -> {body}")
            except json.JSONDecodeError:
                print("Error decoding SQS message body:", record["body"])
                continue

        if message_body:
            response = sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(message_body),
            )

            print(f"Message sent to SQS: {response['MessageId']}")

    return {
        "statusCode": 200,
        "body": "Processed Successfully"
    }
