import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Groups')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    group_id = f"group-{str(uuid.uuid4())[:4]}"
    group_info = {
        'group_id': group_id,
        'members': event.get('members').replace(' ', '').split(',')
    }
    table.put_item(Item=group_info)
    return {
        'statusCode': 200,
        'body': json.dumps({'group_id': group_id})
    }