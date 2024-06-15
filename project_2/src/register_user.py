import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    user_id = f"user-{str(uuid.uuid4())[:4]}"
    password = event['password']
    user_info = {
        'user_id': user_id,
        'password': password,
        'blocked_users': []
    }
    table.put_item(Item=user_info)

    return {
        'statusCode': 200,
        'body': json.dumps({'user_id': user_id})
    }