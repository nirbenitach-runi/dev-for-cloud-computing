import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Groups')

def lambda_handler(event, context):
    group_id = str(uuid.uuid4())
    group_info = {
        'group_id': group_id,
        'group_name': event['group_name'],
        'members': event.get('members', [])
    }
    table.put_item(Item=group_info)
    return {'statusCode': 200, 'body': {'group_id': group_id}}