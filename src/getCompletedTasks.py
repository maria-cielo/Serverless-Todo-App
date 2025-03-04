import json
import boto3
import logging
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TodosNew")


def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    query_params = event.get("queryStringParameters", {})
    logger.info(f"Query String Parameters: {json.dumps(query_params)}")
    completed_status = query_params.get("completed")

    if completed_status is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing 'completed' query param"})
        }

    completed_status = "true" if completed_status.lower() == "true" else "false"

    ## query() is for partition keys (PK) and sort keys (SK)
    # response = table.query(
    #     IndexName="completed-task-index",
    #     KeyConditionExpression=Key("completed").eq(completed_status)
    # )

    response = table.scan(
        IndexName="completed-task-index",
        FilterExpression=Attr("completed").eq(completed_status)
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Items", []))
    }