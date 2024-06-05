import boto3
import uuid
import time

dynamodb = boto3.resource('dynamodb')
groups_table = dynamodb.Table('Groups')
users_table = dynamodb.Table('Users')
messages_table = dynamodb.Table('Messages')

def lambda_handler(event, context):
    sender_id = event['sender_id']
    group_id = event['group_id']
    message = event['message']
    
    # Check if sender is part of the group
    response = groups_table.get_item(Key={'group_id': group_id})
    if 'Item' in response and sender_id in response['Item'].get('members', []):
        members = response['Item']['members']
        timestamp = int(time.time())
        
        for member_id in members:
            # Check if sender is blocked by the member
            user_response = users_table.get_item(Key={'user_id': member_id})
            if 'Item' in user_response and sender_id in user_response['Item'].get('blocked_users', []):
                continue  # Skip this member if the sender is blocked
            
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
        
        return {'statusCode': 200, 'body': 'Message sent to group members'}
    
    return {'statusCode': 403, 'body': 'Sender is not a member of the group'}