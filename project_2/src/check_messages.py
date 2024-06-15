import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
messages_table = dynamodb.Table('Messages')
users_table = dynamodb.Table('Users')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    user_id = event['user_id']
    password = event['password']

    # Verify user credentials before querying messages
    response = users_table.get_item(Key={'user_id': user_id})
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'User not found'})
        }
    
    stored_password = response['Item'].get('password')
    if stored_password != password:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Unauthorized access'})
        }
    
    response = messages_table.query(
        IndexName='receiver_id-index',
        KeyConditionExpression=Key('receiver_id').eq(user_id)
    )
    
    response = messages_table.query(
        IndexName='receiver_id-index',
        KeyConditionExpression=Key('receiver_id').eq(user_id)
    )
    
    messages = response.get('Items', [])
    formatted_messages = []
    for message in messages:
        formatted_message = {
            'timestamp': datetime.fromtimestamp(int(message['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
            'sender_id': message.get('sender_id'),
            'message': message.get('message')
        }
        formatted_messages.append(formatted_message)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'messages': formatted_messages})
    }