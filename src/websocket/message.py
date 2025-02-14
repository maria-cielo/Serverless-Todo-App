import boto3
import json


dynamodb = boto3.resource("dynamodb")
APIGW_MANAGEMENT_API = "https://9ae175ij6c.execute-api.us-east-1.amazonaws.com/dev"
api_gateway = boto3.client("apigatewaymanagementapi", endpoint_url=APIGW_MANAGEMENT_API)


def lambda_handler(event, context):
    body = json.loads(event["body"])
    message = body.get("message", "")

    table = dynamodb.Table("WebSocketConnections")
    connections = table.scan()["Items"]

    for connection in connections:
        connection_id = connection["connectionId"]
        api_gateway.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps({"message": message})
        )

    return {"statusCode": 200}