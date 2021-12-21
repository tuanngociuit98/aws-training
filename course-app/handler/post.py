import json
import boto3
import os
import datetime

now = datetime.datetime.now()
local_now = now.astimezone()
dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    if "body" not in event:
        return {"message": "Something went wrong"}
    
    body = json.loads(event["body"])
    

    params = {
        "course_id": {"S":body["course_id"]},
        "title":{"S":body["title"]}, 
        "description":{"S":body["description"]},
        "teacher":{"S":body["teacher"]},
        "created":{"S":str(local_now)},
        "updated":{"S":str(local_now)}
    }  
    response = dynamodb.put_item(TableName = os.environ['TABLE_NAME'], Item=params)
    
    return {
       "statusCode": 200,
        "body": json.dumps({
            "message": "Data insert success",
        }),
    }