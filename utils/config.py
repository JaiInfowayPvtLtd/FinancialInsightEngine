import json
import os
import logging

def load_config():
    """
    Load configuration settings from environment variables or default values
    
    Returns:
        dict: Configuration settings
    """
    config = {
        # AWS Configuration
        'aws_region': os.environ.get('AWS_REGION', 'us-east-1'),
        'use_ses': os.environ.get('USE_SES', 'false').lower() == 'true',
        'use_bedrock': os.environ.get('USE_BEDROCK', 'false').lower() == 'true',
        
        # Email Configuration
        'sender_email': os.environ.get('SENDER_EMAIL', 'financial-assistant@example.com'),
        
        # Agent Configuration
        'supervisor_agent_id': os.environ.get('SUPERVISOR_AGENT_ID', ''),
        'portfolio_agent_id': os.environ.get('PORTFOLIO_AGENT_ID', ''),
        'data_agent_id': os.environ.get('DATA_AGENT_ID', ''),
        
        # Lambda Configuration
        'lambda_base_url': os.environ.get('LAMBDA_BASE_URL', 'http://localhost:8000'),
        'portfolio_lambda_name': os.environ.get('PORTFOLIO_LAMBDA_NAME', 'portfolio-assistant'),
        
        # Knowledge Base Configuration
        'knowledge_base_id': os.environ.get('KNOWLEDGE_BASE_ID', ''),
        'fomc_data_path': os.environ.get('FOMC_DATA_PATH', 'data/fomc_summaries.json'),
        
        # Logging Configuration
        'log_level': os.environ.get('LOG_LEVEL', 'INFO'),
    }
    
    # Configure logging
    numeric_level = getattr(logging, config['log_level'].upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logging.info("Configuration loaded")
    return config
