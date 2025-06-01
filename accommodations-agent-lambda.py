'''
Accomodation AI Agent: Smart Hotel & Airbnb Discovery
This AWS Bedrock-powered AI agent, built with Lambda and API Gateway, 
provides users with tailored hotel and Airbnb recommendations by retrieving and 
filtering location-based accommodations from an Amazon S3 dataset.
Key Features:
- Dynamic Accommodation Search: Lists hotels or Airbnbs based on user-input location.
- Customizable Preferences: Filters Airbnb options based on pet-friendliness, pool availability, 
and sauna features for personalized recommendations.
- Efficient Data Processing: Reads and processes CSV data from S3 buckets, ensuring accurate results.
- Structured JSON Responses: Returns hotel and Airbnb options in a clean, structured format for seamless integration.
- Error Handling & Logging: Implements robust error detection and logging for reliable performance.
This solution enables seamless travel planning through real-time data retrieval and intelligent filtering, 
perfect for booking assistants or hospitality service automation.
'''
import logging
import json
from typing import Dict, Any
from http import HTTPStatus
import boto3
import pandas as pd
from io import StringIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_bucket = "restaurant-agents-bucket"
hotel_csv = "hotel.csv"
airbnb_csv = "airbnb.csv"

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for processing Bedrock agent requests.
    
    Args:
        event (Dict[str, Any]): The Lambda event containing action details
        context (Any): The Lambda context object
    
    Returns:
        Dict[str, Any]: Response containing the action execution results
    
    Raises:
        KeyError: If required fields are missing from the event
    """
    print("Lamda function statrted")
    
    try:
        agent = event.get('agent', '')
        action_group = event.get('actionGroup', '')
        function = event.get('function', '')
        parameters = event.get('parameters', [])
        message_version = event.get('messageVersion',1) 

        param_dict = {param['name']: param['value'] for param in parameters}

        if function == "list-hotels":
            location = param_dict.get('location', None)
            print(location) # log results
            s3_key = hotel_csv
            filter_column = "Location"
            fitlers = {filter_column: location}
        elif function == "list-airbnbs":
            location = param_dict.get('location', None)
            pets = param_dict.get('pets', None)
            pool = param_dict.get('pool', None)
            sauna = param_dict.get('sauna', None)
            print(location, pets, pool, sauna) # log results
            s3_key = airbnb_csv
            fitlers = {'Location': location, 'Pets': pets, 'Pool': pool, 'Sauna': sauna}
        else:
            return {"error": "Invalid function name"}

        # Import hotel and airbnb data
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)

        csv_data = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))
        
        df.map(lambda x: x.strip().lower() if isinstance(x, str) else x) # strip all strings

        for col, val in fitlers.items():
            if val is not None:
                df = df[df[col].astype(str).str.lower() == str(val).lower()]

        # Give results to Agent
        filtered_data = json.dumps(df.to_dict(orient='records'), default=str)
        print(filtered_data)

        response_body = {
            'TEXT': {
                'body': filtered_data
            }
        }
        action_response = {
            'agent': agent,
            'actionGroup': action_group,
            'function': function,
            'functionResponse': {
                'responseBody': response_body
            }
        }
        response = {
            'response': action_response,
            'messageVersion': message_version
        }

        dummy_function_response = {
        'response': action_response,
        'messageVersion': message_version,
        'statusCode': HTTPStatus.OK,
        'body': 'Dummy function executed successfully'
        }

        return dummy_function_response

        logger.info('Response: %s', response)
        return response

    except KeyError as e:
        logger.error('Missing required field: %s', str(e))
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': f'Error: {str(e)}'
        }
    except Exception as e:
        print(e)
        logger.error('Unexpected error: %s', str(e))
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error processing the request, error: {e}')
        }
