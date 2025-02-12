import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodoTable")

def update_todo(event, context):
    todo_id = event["pathParameters"]["id"]
    data = json.loads(event["body"])
    result = table.update_item(
        Key={"id": todo_id},
        UpdateExpression="set task=:t, completed=:c",
        ExpressionAttributeValues={
            ":t": data["task"],
            ":c": data["completed"]
        },
        ReturnValues="UPDATED_NEW"
    )
    response = {
        "statusCode": 200,
        "body": json.dumps(result["Attributes"])
    }
    return response