import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    user_id = f"user-{str(uuid.uuid4())[:4]}"
    user_info = {
        'user_id': user_id,
        'blocked_users': []
    }
    table.put_item(Item=user_info)

    return {
        'statusCode': 200,
        'body': json.dumps({'user_id': user_id})
    }