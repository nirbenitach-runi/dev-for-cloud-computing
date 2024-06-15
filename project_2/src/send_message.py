import json
import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')
messages_table = dynamodb.Table('Messages')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    sender_id = event['sender_id']
    password = event['password']
    receiver_id = event['receiver_id']
    message = event['message']
    
    response_sender = users_table.get_item(Key={'user_id': sender_id})
    if 'Item' not in response_sender:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Sender ID not found.'})
        }
    stored_password = response_sender['Item'].get('password')
    
    if stored_password != password:
        return {
            'statusCode': 403,
            'body': json.dumps({'message': 'Unauthorized access'})
        }
    
    response_receiver = users_table.get_item(Key={'user_id': receiver_id})
    if 'Item' in response_receiver and sender_id in response_receiver['Item'].get('blocked_users', []):
        return {
            'statusCode': 403,
            'body': json.dumps({'message': f'You are unable to send messages to {receiver_id}.'})
        }
    
    message_id = str(uuid.uuid4())
    message_info = {
        'message_id': message_id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message,
        'timestamp': int(time.time())
    }
    messages_table.put_item(Item=message_info)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Message sent to {receiver_id}.'})
    }