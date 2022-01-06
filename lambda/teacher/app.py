import json
import boto3 
import os
# import requests'


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    tableName = dynamodb.Table('teacherTable')
    kinesis = boto3.client('kinesis')
    
    def recordUpdateTeacherName(old_name, new_name):
        kinesis.put_record(
        StreamName= 'kinesisStream',
        Data = json.dumps({
            'old_teacher_name' :old_name,
            'new_teacher_name' :new_name
        }),
        PartitionKey = 'filter'
    )
    
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
            "teacherId":body["teacherId"],
            "teacherName":body["teacherName"],
            "gender":body["gender"],
            "date_of_birth":body["date_of_birth"]
            
        })
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done",
            
        }),
    } 
    if event["httpMethod"] == "DELETE":
        data = event["multiValueQueryStringParameters"]["teacherId"]
        response = tableName.delete_item(
            Key = {
                "teacherId": data[0]
            }
        )
        
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": data,
            
        })}
        
    if event["httpMethod"] == "PATCH":
        data = event["multiValueQueryStringParameters"]["teacherId"]
        newTeacher = json.loads(event["body"])
        getCurrentTeacher = tableName.get_item(
        Key={
            'teacherId': data[0],
        },)
        oldTeacher = getCurrentTeacher["Item"]
       
        
        if oldTeacher["teacherName"]!= newTeacher["teacherName"]:
            recordUpdateTeacherName(oldTeacher["teacherName"],newTeacher["teacherName"])
            
        
            
        response = tableName.update_item(
            Key={
            'teacherId': data[0],
        },
            UpdateExpression="set teacherName =:t, gender=:g, date_of_birthd=:d",
            ExpressionAttributeValues={
              ':t': newTeacher["teacherName"],
              ':g': newTeacher["gender"],
              ':d': newTeacher['date_of_birth']
            },
            ReturnValues="UPDATED_NEW"
    
          )
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done",
            
        })}          