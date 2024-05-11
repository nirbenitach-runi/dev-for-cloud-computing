import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ParkingLotTable')

def lambda_handler(event, context):
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
            'body': json.dumps({'message': f'Unable to access {ticket_id}, something went wrong: {repr(e)}'})
        } 
    
    if entry:
        entry_time = datetime.strptime(entry['entry_time'], "%Y-%m-%d %H:%M:%S")
        exit_time = datetime.now()
        parked_time = exit_time - entry_time
        total_hours = parked_time.total_seconds() / 3600
        total_charge = calculate_charge(total_hours)
        
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

def get_entry(ticket_id):
    response = table.get_item(Key={'ticket_id': ticket_id})
    return response.get('Item')

def calculate_charge(total_hours):
    total_charge = total_hours * 10
    total_charge += 10 * ((total_hours * 60) % 15 > 0)
    return "${:.2f}".format(total_charge)