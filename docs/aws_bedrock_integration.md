# AWS Bedrock Integration Guide

This guide provides instructions for enhancing the Financial Assistant with actual Amazon Bedrock services instead of the local simulation currently implemented.

## Overview

The Financial Assistant application is designed to simulate Amazon Bedrock's multi-agent collaboration framework. To use actual AWS Bedrock services, you'll need to:

1. Set up the necessary AWS resources
2. Configure Bedrock agents and knowledge bases
3. Modify the application code to use Bedrock APIs instead of simulations

## Prerequisites

- AWS account with access to Bedrock service
- AWS CLI installed and configured
- IAM user with appropriate permissions
- Familiarity with Amazon Bedrock service

## Setting Up Amazon Bedrock

### 1. Enable Access to Amazon Bedrock

Before using Bedrock, you need to request access to the models:

1. Navigate to the Amazon Bedrock console
2. Go to "Model access" in the left navigation pane
3. Select the models you want to use (e.g., Amazon Titan)
4. Click "Request access"
5. Wait for approval (usually immediate)

### 2. Create a Knowledge Base

A knowledge base is required for the Data Assistant to access financial information:

1. In the Amazon Bedrock console, go to "Knowledge bases"
2. Click "Create knowledge base"
3. Configure the knowledge base:
   - Name: "FinancialDataKB"
   - Description: "Knowledge base for financial data and FOMC reports"
   - Choose Amazon Titan Embeddings as the embedding model
4. Create an Amazon S3 bucket to store your documents
5. Upload the financial PDFs and FOMC reports to the S3 bucket
6. Configure the data source to point to your S3 bucket
7. Set up an IAM role with permissions to access the bucket
8. Complete the creation process and note the knowledge base ID

### 3. Create Bedrock Agents

You'll need to create three agents:

#### Supervisor Agent

1. In the Amazon Bedrock console, go to "Agents"
2. Click "Create agent"
3. Configure the agent:
   - Name: "FinancialSupervisorAgent"
   - Description: "Main agent for orchestrating financial requests"
   - Choose Amazon Titan as the foundation model
   - Configure agent instructions to match the orchestration logic
4. Set up action groups to call the specialized agents
5. Configure security and permissions
6. Test and publish the agent
7. Note the agent ID

#### Portfolio Assistant Agent

1. Create another agent named "PortfolioAssistantAgent"
2. Configure foundation model and instructions for portfolio creation
3. Set up action groups for:
   - Creating portfolios
   - Researching companies
   - Sending emails
4. Configure API schemas matching the Lambda function
5. Set up security and permissions
6. Test and publish the agent
7. Note the agent ID

#### Data Assistant Agent

1. Create an agent named "DataAssistantAgent"
2. Configure foundation model and instructions for financial data handling
3. Connect to the knowledge base created earlier
4. Set up action groups for:
   - Querying financial data
   - Summarizing FOMC reports
5. Test and publish the agent
6. Note the agent ID

## Integrating Bedrock with the Application

### 1. Update the Config File

Modify `utils/config.py` to include Bedrock-specific configurations:

```python
def load_config():
    config = {
        # Existing configuration...
        
        # Bedrock Configuration
        'use_bedrock': os.environ.get('USE_BEDROCK', 'false').lower() == 'true',
        'supervisor_agent_id': os.environ.get('SUPERVISOR_AGENT_ID', ''),
        'portfolio_agent_id': os.environ.get('PORTFOLIO_AGENT_ID', ''),
        'data_agent_id': os.environ.get('DATA_AGENT_ID', ''),
        'knowledge_base_id': os.environ.get('KNOWLEDGE_BASE_ID', ''),
        'bedrock_region': os.environ.get('BEDROCK_REGION', 'us-east-1'),
        
        # Additional configuration...
    }
    
    # Rest of the function...
    return config
```

### 2. Enhance AWS Service Class

Update `utils/aws_service.py` to use actual Bedrock APIs:

```python
def invoke_bedrock_agent(self, agent_id, prompt):
    """
    Invoke an Amazon Bedrock agent with a prompt
    
    Args:
        agent_id (str): ID of the Bedrock agent
        prompt (str): User prompt to send to the agent
        
    Returns:
        dict: Agent response
    """
    if not self.config.get('use_bedrock', False) or not agent_id:
        return self._simulate_bedrock_response(prompt)
        
    try:
        # Get AWS credentials
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        
        # Create Bedrock Runtime client
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=self.config.get('bedrock_region', 'us-east-1'),
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
            agentAliasId='TSTALIASID', # Use your actual alias ID
            sessionId=str(uuid.uuid4()),
            inputText=json.dumps(request_body)
        )
        
        # Process the response
        response_body = json.loads(response['completion'])
        logging.info(f"Bedrock agent response received: {str(response_body)[:100]}...")
        
        return response_body
        
    except Exception as e:
        logging.error(f"Error invoking Bedrock agent: {str(e)}")
        return self._simulate_bedrock_response(prompt)
```

### 3. Update the Supervisor Agent

Modify `agents/supervisor.py` to leverage the Bedrock agent:

```python
def process_request(self, user_query, user_email=None):
    """
    Process the user query and route to appropriate agent
    
    Args:
        user_query (str): The user's query text
        user_email (str, optional): User's email for sending portfolio
        
    Returns:
        str: Response to the user query
    """
    logging.info(f"Processing user request: {user_query}")
    
    # Try using Bedrock Supervisor Agent if configured
    if self.config.get('use_bedrock', False) and self.config.get('supervisor_agent_id'):
        try:
            aws_service = AWSService(self.config)
            
            # Prepare a prompt that includes context about the request
            prompt = f"User Email: {user_email if user_email else 'Not provided'}\nUser Query: {user_query}"
            
            # Invoke the Bedrock agent
            response = aws_service.invoke_bedrock_agent(
                self.config['supervisor_agent_id'],
                prompt
            )
            
            # Extract the response text
            if response and 'completion' in response:
                return response['completion']
                
        except Exception as e:
            logging.error(f"Error using Bedrock Supervisor Agent: {str(e)}")
            logging.info("Falling back to local processing")
    
    # Fall back to local implementation if Bedrock fails or is not configured
    # Existing code for local processing...
```

### 4. Update the Specialized Agents

Similarly update the Portfolio Assistant and Data Assistant to use Bedrock when available, with fallback to local implementation.

### 5. Configure Environment Variables

Set the necessary environment variables to connect to Bedrock:

```bash
# Bedrock Configuration
export USE_BEDROCK=true
export SUPERVISOR_AGENT_ID=your_supervisor_agent_id
export PORTFOLIO_AGENT_ID=your_portfolio_agent_id
export DATA_AGENT_ID=your_data_agent_id
export KNOWLEDGE_BASE_ID=your_knowledge_base_id
export BEDROCK_REGION=us-east-1
```

## Testing Bedrock Integration

After setting up the integration, test the application:

1. Run the application with Bedrock configuration enabled
2. Monitor logs for API calls to the Bedrock service
3. Test each type of request (portfolio creation, financial insights, FOMC summaries)
4. Compare responses with the simulated implementation

## Production Considerations

When deploying with Bedrock in production:

1. **Cost Management**: Monitor usage of Bedrock services, as they are billed based on usage
2. **Security**: Implement fine-grained IAM policies for Bedrock access
3. **Error Handling**: Enhance error handling for Bedrock API failures
4. **Monitoring**: Set up CloudWatch alarms for Bedrock API errors
5. **Performance**: Monitor response times and optimize prompt design

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify AWS credentials have permission to access Bedrock
   - Check that the IAM policy includes `bedrock:InvokeAgent` permissions

2. **Agent Not Found**:
   - Verify the agent IDs are correct
   - Check that the agents are published and in the correct region

3. **Knowledge Base Issues**:
   - Verify the knowledge base is indexed correctly
   - Check permissions for accessing S3 documents

4. **Rate Limiting**:
   - Implement retry logic with exponential backoff
   - Consider requesting quota increases for production use

### Logging and Debugging

Enable detailed logging for the Bedrock integration:

```python
import logging
import boto3

# Configure detailed logging
logging.basicConfig(level=logging.DEBUG)
boto3.set_stream_logger('botocore', logging.DEBUG)
```

## Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Bedrock Agents Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Bedrock Knowledge Base Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Boto3 Bedrock Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)