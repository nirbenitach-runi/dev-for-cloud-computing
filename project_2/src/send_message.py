import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')
messages_table = dynamodb.Table('Messages')

def lambda_handler(event, context):
    sender_id = event['sender_id']
    receiver_id = event['receiver_id']
    message = event['message']
    
    # Check if sender is blocked
    response = users_table.get_item(Key={'user_id': receiver_id})
    if 'Item' in response and sender_id in response['Item'].get('blocked_users', []):
        return {'statusCode': 403, 'body': 'Sender is blocked'}
    
    message_id = str(uuid.uuid4())
    message_info = {
        'message_id': message_id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'message': message,
        'timestamp': int(time.time())
    }
    messages_table.put_item(Item=message_info)
    return {'statusCode': 200, 'body': 'Message sent'}