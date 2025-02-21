def lambda_handler(event, context):
    for record in event["Records"]:
        message_body = record["body"]
        print(f"Message Received: {message_body}")

    return {
        "statusCode": 200,
        "body": "Processed Successfully"
    }