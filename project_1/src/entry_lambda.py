import json
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingLotTable')

def lambda_handler(event, context):
    """ Lambda function entry point. Handles incoming requests to register parking lot entries. """
    try:
        plate = event['queryStringParameters']['plate']
        parking_lot = event['queryStringParameters']['parkingLot']
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Something went wrong with your request: {repr(e)}'})
        } 

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