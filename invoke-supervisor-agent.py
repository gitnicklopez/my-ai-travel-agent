'''
Supervisor AI Agent: Real-Time Chat Processing
This AWS Lambda function enables seamless interactions with a Bedrock-powered AI agent, 
processing user text inputs and returning real-time AI-generated responses.

Key Features:
- Dynamic Text Processing: Receives user input and invokes the AI agent to generate responses.
- Session Management: Maintains conversation flow using unique sessionId values.
- AWS Bedrock Integration: Uses invoke_agent() to interact with preconfigured Bedrock AI models.
- Error Handling & Logging: Implements robust exception handling for uninterrupted service.
- Optimized Data Processing: Converts responses efficiently and returns structured JSON output.

This solution enables smooth AI-driven interactions for customer service, virtual assistance, and conversational AI applications.
'''
import json
import boto3

def lambda_handler(event, context):
    
    data = event['body']
    client = boto3.client('bedrock-agent-runtime')

    data_dict = json.loads(data)
    input_text = data_dict['text']
    session_id = data_dict['sessionId']

    try:
        response = client.invoke_agent(
            agentId="SKVTN8GZY6",
            agentAliasId= "DR6ZKQTJGE",
            sessionId=session_id,
            inputText=input_text,
            endSession = False
        )

        response_text = ""

        for event in response['completion']:
            if "chunck" in event and "bytes" in event['chunk']:
                response_text += event['chunk']['bytes'].decode('utf8')
        print(response_text)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': response_text
            })
        }    
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
