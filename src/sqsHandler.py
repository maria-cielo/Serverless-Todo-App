import json


def lambda_handler(event, context):
    for record in event["Records"]:
        try:
            # SQS message body
            message_body = json.loads(record["body"])
            action = message_body.get("action", "UNKNOWN")
            todo_id = message_body.get("todo_id", None)
            data = message_body.get("data", {})

            print(f"Processing SQS message: {action} for TODO ID {todo_id}")

        except json.JSONDecodeError as e:
            print(f"Error decoding SQS message: {str(e)}")
            continue

    return {
        "statusCode": 200,
        "body": json.dumps("SQS message processed successfully!")
    }