import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Groups')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    group_id = event['group_id']
    user_id = event['user_id']
    action = event['action']  # 'add' or 'remove'
    
    response = table.get_item(Key={'group_id': group_id})
    if 'Item' in response:
        members = response['Item'].get('members', [])
        if action == 'add' and user_id not in members:
            members.append(user_id)
            action_string = "added to"
        elif action == 'remove' and user_id in members:
            members.remove(user_id)
            action_string = "removed from"
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Invalid action or user already in desired state.'})
            }
        
        table.update_item(
            Key={'group_id': group_id},
            UpdateExpression='SET members = :members',
            ExpressionAttributeValues={':members': members}
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'{user_id} has been {action_string} the group.'})
        }
    
    return {
        'statusCode': 400,
        'body': json.dumps({'message': f'Group ({group_id}) not found.'})
    }