import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    user_id = event['user_id']
    block_user_id = event['block_user_id']
    
    response = table.get_item(Key={'user_id': user_id})
    if 'Item' in response:
        blocked_users = response['Item'].get('blocked_users', [])
        if block_user_id not in blocked_users:
            blocked_users.append(block_user_id)
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET blocked_users = :blocked_users',
                ExpressionAttributeValues={':blocked_users': blocked_users}
            )
            return {'statusCode': 200, 'body': 'User blocked'}
    
    return {'statusCode': 400, 'body': 'User not found'}