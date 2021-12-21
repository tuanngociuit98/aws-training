import boto3
import json
import os

kinesis = boto3.client('kinesis', region_name='us-west-2')
def update_name_to_stream(old_name, new_name):
    kinesis.put_record(
        StreamName= os.environ['STREAM_NAME'],
        Data = json.dumps({
            'old_teacher_name' :old_name,
            'new_teacher_name' :new_name
        }),
        PartitionKey = 'filter'
    )
    print('succeed stream')