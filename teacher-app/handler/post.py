import json
import boto3
import os

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    if "body" not in event:
        return {"message": "Something went wrong"}
    
    body = json.loads(event["body"])

    params = {
        "teacher_id": {"S":body["teacher_id"]},
        "teacher_name":{"S":body["teacher_name"]}, 
        "date_of_birth":{"S":body["date_of_birth"]}, 
        "gender":{"S":body["gender"]}
    }  
    response = dynamodb.put_item(TableName = os.environ['TABLE_NAME'], Item=params)
    
    return {
       "statusCode": 200,
        "body": json.dumps({
            "message": "Data insert success",
        }),
    }