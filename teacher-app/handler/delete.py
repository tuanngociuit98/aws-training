import json
import boto3
import os

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    teacher_id = event["pathParameters"]["teacher_id"]
    response = dynamodb.delete_item(
        TableName = os.environ['TABLE_NAME'],
        Key={
            "teacher_id": {'S':teacher_id}
        }
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Delete success",
        }),
    }
