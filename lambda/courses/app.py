import json
import boto3 
# import requests

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    tableName = dynamodb.Table('coursesTable')
    kinesis = boto3.client('kinesis')
    data = tableName.scan()
  
    
    if event["httpMethod"] == "GET" : 
        return {
      'statusCode': 200,
      'body': json.dumps(data["Items"]),
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },  
  }
    if event["httpMethod"] == "POST" : 
       
        body    = json.loads(event["body"])
        tableName.put_item(Item = {
            "courseId":body["courseId"],
            "courseName":body["courseName"],
            "price":body["price"],
            "teacher":body["teacher"]
            
        })
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done",
            
        }),
    } 
    if event["httpMethod"] == "DELETE":
        data = event["multiValueQueryStringParameters"]["courseId"]
        response = tableName.delete_item(
            Key = {
                "courseId": data[0]
            }
        )
        
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": data,
            
        })}
        
    if event["httpMethod"] == "PATCH":
        data = event["multiValueQueryStringParameters"]["courseId"]
        body = json.loads(event["body"])
        courseName = body["courseName"]
        price = body["price"]
        teacher = body["teacher"]
        response = tableName.update_item(
        Key={
            'courseId': data[0],
        },
        UpdateExpression="set courseName =:n, price=:p, teacher=:t",
        ExpressionAttributeValues={
            ':n': courseName,
            ':p': price,
            ':t': teacher
        },
        ReturnValues="UPDATED_NEW"
    
        )
        
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done",
            
        })}        
        

     
   

    
    