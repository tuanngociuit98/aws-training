import boto3
import json
import os

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    
    response = dynamodb.scan(TableName = os.environ['TABLE_NAME'])
    print(response)
    
    if (response['Count'] > 0) :
        return {
            "statusCode" : 200,
            "body": json.dumps({
                "message": "Get "+str(response['Count'])+ " Teachers success",
                "body": response['Items'] 
            })
        }
    else:
        return {
            "statusCode" : 200,
            "body": json.dumps({
                "message": "There is no teacher",
            })
        }