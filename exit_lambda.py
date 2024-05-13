import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingLotTable')

def lambda_handler(event, context):
    """ Lambda function entry point. Handles incoming requests to process parking lot exits. """
    try:
        ticket_id = event['queryStringParameters']['ticketId']
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Something went wrong with your request: {repr(e)}'})
        } 

    try:
        entry = get_entry(ticket_id)
    except Exception as e:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': f'Unable to access ticket ID: {ticket_id}, something went wrong: {repr(e)}'})
        } 
    
    if entry:
        entry_time = datetime.strptime(entry['entry_time'], "%Y-%m-%d %H:%M:%S")
        exit_time = datetime.now()
        parked_time = exit_time - entry_time
        total_minutes = parked_time.total_seconds() / 60
        total_charge = calculate_charge(total_minutes=total_minutes)
        
        table.delete_item(Key={'ticket_id': ticket_id})
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'license_plate': entry['license_plate'],
                'parked_time': str(parked_time),
                'parking_lot': entry['parking_lot'],
                'charge': total_charge
            })
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Entry not found for the provided ticket ID'})
        }

def get_entry(ticket_id: str) -> dict:
    """ Retrieve parking entry details from the database. """
    response = table.get_item(Key={'ticket_id': ticket_id})
    return response.get('Item')

def calculate_charge(total_minutes: float, price_per_hour: float = 10.0, time_increment_in_minutes: float = 15.0) -> str:
    """ Calculate parking charge based on parking duration and predefined rates. """
    total_charge = (total_minutes // time_increment_in_minutes) * (price_per_hour / (60 / time_increment_in_minutes))
    return "${:.2f}".format(total_charge)