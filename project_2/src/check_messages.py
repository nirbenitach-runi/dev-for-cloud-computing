import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Messages')

def lambda_handler(event, context):
    user_id = event['user_id']
    
    response = table.query(
        IndexName='receiver_id-index',
        KeyConditionExpression=Key('receiver_id').eq(user_id)
    )
    
    messages = response.get('Items', [])
    return {'statusCode': 200, 'body': messages}