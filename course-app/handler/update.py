import json
import boto3
import os
import datetime

now = datetime.datetime.now()
local_now = now.astimezone()

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    if "body" not in event:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No data",
            }),
        }
    course_id = event["pathParameters"]["course_id"]

    body = json.loads(event["body"])
    
    if course_id:
        body["course_id"] = course_id
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No id found",
            }),
        }

    params = {
        "course_id": {"S":body["course_id"]},
        "title":{"S":body["title"]}, 
        "teacher":{"S":body["teacher"]},
        "description":{"S":body["description"]},
        "updated":{"S":str(local_now)}
    }  
    
    response = dynamodb.put_item(TableName = os.environ['TABLE_NAME'], Item=params)
    
    return {
       "statusCode": 201,
        "body": json.dumps({
            "message": "Data update success",
        }),
    }