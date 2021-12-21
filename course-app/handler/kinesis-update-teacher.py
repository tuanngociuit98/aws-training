import json
import base64
import boto3
import os
import time

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        data = json.loads(payload)
        print(data)
        time.sleep(5)
   
    teacher = dynamodb.query(
        TableName=os.environ['TABLE_NAME'],
        IndexName='Teacher',
        KeyConditionExpression='teacher= :name',
        ExpressionAttributeValues={
            ':name': {"S":data['old_teacher_name']}
        }    
    )
 
    if teacher['Items'] :
        courseId = teacher['Items'][0]['course_id']['S']
        response = dynamodb.update_item(
            TableName = os.environ['TABLE_NAME'],
            Key = {
                'course_id': {'S': courseId}
            },
            UpdateExpression = "teacher=:t",
            ExpressionAttributeValues={
                ':t': {'S':data['new_teacher_name']},
            },
            ReturnValues="UPDATED_NEW"
        )
        print('success')
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Update Name Success",
                "body":response
            }),
        }
    else:
        print('fail')
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "No name found",
            }),
        }
    
   

  