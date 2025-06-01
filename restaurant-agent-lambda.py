'''
Restaurant AI Agent: Smart Dining Assistance
This AI-powered restaurant agent, built using AWS Bedrock, Lambda, and API Gateway, 
enables intelligent dining recommendations and streamlined customer service. Designed to process customer queries dynamically, 
it fetches restaurant data from an Amazon S3 bucket and intelligently filters results based on user preferences.

Core Functionality:
- Efficient Data Retrieval: Extracts restaurant details from an S3 bucket-stored CSV file.
- Intelligent Filtering: Processes city and fine dining preferences for personalized results.
- Scalable & Serverless Architecture: Uses AWS Lambda to ensure responsiveness and minimal infrastructure overhead.
- Structured JSON Responses: Returns processed data in a clean, structured format for seamless integration.
- Error Handling: Logs issues efficiently while maintaining reliability.

This solution optimizes restaurant selection by offering precise filtering and real-time responses, 
making it ideal for automated customer interactions in dining services.
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
S3_KEY = "restaurant.csv"


def lambda_handler(event, context):
    print("Lambda function started")

    try:
        agent = event.get('agent', '')
        actionGroup = event.get('actionGroup', '')
        function = event.get('function', '')
        parameters = event.get('parameters', [])

        param_dict = {param['name']: param['value'] for param in parameters}

        city = param_dict.get('city', None)
        fine_dine = param_dict.get('fine_dine', None)

        print(city, fine_dine)

        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=s3_bucket, Key=S3_KEY)

        csv_data = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))

        df['Fine Dining'] = df['Fine Dining'].str.strip().str.lower()
        df['City'] = df['City'].str.strip().str.lower()

        if city:
            df = df[df['City'] == city.strip().lower()]
        if fine_dine:
            df = df[df['Fine Dining'] == fine_dine.strip().lower()]

        filtered_data = json.dumps(df.to_dict(orient='records'),default = str)

        responseBody = {
            "TEXT": {
                "body": filtered_data,
            }
        }

        action_response = {
            'actionGroup':actionGroup,
            'function': function,
            'functionResponse': {
                'responseBody': responseBody
            }
        }

        dummy_function_response = {'response':action_response, 'messageVersion': event['messageVersion']}

        return dummy_function_response

    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error processing the request, error: {e}]')
        }
