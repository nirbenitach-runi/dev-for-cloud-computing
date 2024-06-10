import json
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Messages')

def lambda_handler(event, context):
    user_id = event['user_id']
    
    response = table.query(
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