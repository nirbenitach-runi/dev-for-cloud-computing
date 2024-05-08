import json
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingLotTable')

def lambda_handler(event, context):
    plate = event['queryStringParameters']['plate']
    parking_lot = event['queryStringParameters']['parkingLot']
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket_id = str(uuid4())
    
    table.put_item(Item={
        'ticket_id': ticket_id,
        'license_plate': plate,
        'entry_time': entry_time,
        'parking_lot': parking_lot
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps({'ticket_id': ticket_id})
    }