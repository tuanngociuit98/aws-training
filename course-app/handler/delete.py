import json
import boto3
import os

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    course_id = event["pathParameters"]["course_id"]
    response = dynamodb.delete_item(
        TableName = os.environ['TABLE_NAME'],
        Key={
            "course_id": {'S':course_id}
        }
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Delete success",
        }),
    }
