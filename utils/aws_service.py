import logging
import os
import json
import boto3
from botocore.exceptions import ClientError

class AWSService:
    """
    Service for interacting with AWS services like Bedrock, Lambda, S3, etc.
    """
    
    def __init__(self, config):
        """
        Initialize the AWS service
        
        Args:
            config (dict): Configuration settings for the service
        """
        self.config = config
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        logging.info("AWS Service initialized")
    
    def invoke_bedrock_agent(self, agent_id, prompt):
        """
        Invoke an Amazon Bedrock agent with a prompt
        
        Args:
            agent_id (str): ID of the Bedrock agent
            prompt (str): User prompt to send to the agent
            
        Returns:
            dict: Agent response
        """
        try:
            # Get AWS credentials from environment variables
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            
            # Create Bedrock Runtime client
            bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
            
            # Prepare request body
            request_body = {
                "inputText": prompt,
                "enableTrace": True
            }
            
            # Invoke the agent
            response = bedrock_client.invoke_agent(
                agentId=agent_id,
                agentAliasId='TSTALIASID', # This would be configured properly in a real setup
                sessionId='test-session-001',
                inputText=json.dumps(request_body)
            )
            
            # Process the response
            response_body = json.loads(response['completion'])
            logging.info(f"Bedrock agent response received: {str(response_body)[:100]}...")
            
            return response_body
            
        except ClientError as e:
            logging.error(f"Failed to invoke Bedrock agent: {str(e)}")
            
            # Return a simulated response for development
            return self._simulate_bedrock_response(prompt)
        except Exception as e:
            logging.error(f"Unexpected error invoking Bedrock agent: {str(e)}")
            return {"error": str(e)}
    
    def invoke_lambda_function(self, function_name, payload):
        """
        Invoke an AWS Lambda function
        
        Args:
            function_name (str): Name of the Lambda function
            payload (dict): Payload to send to the function
            
        Returns:
            dict: Lambda function response
        """
        try:
            # Get AWS credentials from environment variables
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            
            # Create Lambda client
            lambda_client = boto3.client(
                'lambda',
                region_name=self.aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
            
            # Invoke the function
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            # Process the response
            response_payload = json.loads(response['Payload'].read().decode())
            logging.info(f"Lambda function response received: {str(response_payload)[:100]}...")
            
            return response_payload
            
        except ClientError as e:
            logging.error(f"Failed to invoke Lambda function: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"Unexpected error invoking Lambda function: {str(e)}")
            return {"error": str(e)}
    
    def _simulate_bedrock_response(self, prompt):
        """
        Simulate a Bedrock agent response for development/testing
        
        Args:
            prompt (str): The user prompt
            
        Returns:
            dict: Simulated response
        """
        # Simple response simulation based on prompt keywords
        prompt_lower = prompt.lower()
        
        if "portfolio" in prompt_lower:
            return {
                "completion": "I can help you create an investment portfolio. Please specify which industry you're interested in and how many companies you'd like to include."
            }
        elif "financial data" in prompt_lower or "insights" in prompt_lower:
            return {
                "completion": "I can provide financial insights and data analysis. What specific information are you looking for?"
            }
        elif "fomc" in prompt_lower or "federal reserve" in prompt_lower:
            return {
                "completion": "I can summarize the latest FOMC report for you. The Federal Reserve has maintained its policy stance with a focus on inflation and employment targets."
            }
        else:
            return {
                "completion": "I'm your financial assistant powered by Amazon Bedrock. I can help with portfolio creation, financial insights, and FOMC report summaries. How can I assist you today?"
            }
