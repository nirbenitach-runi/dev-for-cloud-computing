import json
import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')
groups_table = dynamodb.Table('Groups')
users_table = dynamodb.Table('Users')
messages_table = dynamodb.Table('Messages')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    sender_id = event['sender_id']
    password = event['password']
    group_id = event['group_id']
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
    
    response_group = groups_table.get_item(Key={'group_id': group_id})
    if 'Item' in response_group and sender_id in response_group['Item'].get('members', []):
        members = response_group['Item']['members']
        timestamp = int(time.time())
        
        for member_id in members:
            user_response = users_table.get_item(Key={'user_id': member_id})
            if 'Item' in user_response and sender_id in user_response['Item'].get('blocked_users', []):
                continue 
            
            message_id = str(uuid.uuid4())
            message_info = {
                'message_id': message_id,
                'receiver_id': member_id,
                'group_id': group_id,
                'sender_id': sender_id,
                'message': message,
                'timestamp': timestamp
            }
            messages_table.put_item(Item=message_info)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Message sent to {group_id}.'})
        }
    
    return {
        'statusCode': 403,
        'body': json.dumps({'message': f'You are not a member of {group_id}.'})
    }