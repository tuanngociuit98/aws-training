import json
import boto3
import base64

def lambda_handler(event, context):
        dynamodb = boto3.resource('dynamodb')
        tableName = dynamodb.Table('coursesTable')
        kinesis = boto3.client('kinesis') 
        
        for record in event["Records"]:
            payload = base64.b64decode(record["kinesis"]["data"])
            result  = json.loads(payload)
            old_teacher_name = result["old_teacher_name"]
            new_teacher_name = result["new_teacher_name"]
        
        data = tableName.scan()
        courseUpdate = 0
        listCourse = data["Items"]
        for course in listCourse:
            if course["teacher"] == old_teacher_name:
                tableName.update_item(
                  Key={
                    'courseId': course["courseId"],
                     },
                 UpdateExpression="set teacher=:t",
                 ExpressionAttributeValues={
            
            ':t': new_teacher_name
        },
        ReturnValues="UPDATED_NEW"
    
        )
                
            
        
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done",
            
        })
            
        }          
        
    
        
    
        
    
   

    
    