import json
import boto3
from boto3.dynamodb.conditions import Key
import os
from update_name_to_stream import update_name_to_stream

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    if "body" not in event:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No data",
            }),
        }
    teacher_id = event["pathParameters"]["teacher_id"]

    body = json.loads(event["body"])
    
    if teacher_id:
        body["teacher_id"] = teacher_id
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No id found",
            }),
        }

    params = {
        "teacher_id": {"S":body["teacher_id"]},
        "teacher_name":{"S":body["teacher_name"]}, 
        "date_of_birth":{"S":body["date_of_birth"]}, 
        "gender":{"S":body["gender"]}
    }  
    
    check_name_query = dynamodb.query(
        TableName = os.environ['TABLE_NAME'],
        KeyConditions={
        'teacher_id':{
            'AttributeValueList':[
                {
                    'S':teacher_id,
                }
            ],
            'ComparisonOperator': 'EQ'
        }
    }
    )
    
    if (check_name_query['Items'][0]['teacher_name']['S'] != body["teacher_name"]):
        print("check")
        update_name_to_stream(
            check_name_query['Items'][0]['teacher_name']['S'],
            body["teacher_name"]
        )
    
    response = dynamodb.put_item(TableName = os.environ['TABLE_NAME'], Item=params)
    
    return {
       "statusCode": 201,
        "body": json.dumps({
            "message": "Data update success",
        }),
    }
    
