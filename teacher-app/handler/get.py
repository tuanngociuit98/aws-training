import json
import boto3
import os

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):   
    teacher_id = event["pathParameters"]["teacher_id"]
    response = dynamodb.get_item(
        TableName = os.environ['TABLE_NAME'],
        Key={
            "teacher_id": {'S':teacher_id}
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
                "message": "Teacher not found"
            })
        }
