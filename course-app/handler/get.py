import json
import boto3
import os

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):   
    course_id = event["pathParameters"]["course_id"]
    response = dynamodb.get_item(
        TableName = os.environ['TABLE_NAME'],
        Key={
            "course_id": {'S':course_id}
        }
    )
    print(response)
    if (response["Item"]):
        return {
            "statusCode": 200,
            "body": json.dumps(response["Item"])
        }
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "course not found"
            })
        }
