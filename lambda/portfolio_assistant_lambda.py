import json
import logging
import os
import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    """
    AWS Lambda handler function for portfolio assistant
    
    Args:
        event (dict): Lambda event data
        context (LambdaContext): Lambda context
        
    Returns:
        dict: Response containing portfolio data or status
    """
    logger.info("Portfolio Assistant Lambda invoked")
    
    # Extract HTTP method and path
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '')
    
    # Parse request body if it exists
    body = {}
    if 'body' in event and event['body']:
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            logger.error("Failed to parse request body as JSON")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON in request body'})
            }
    
    # Route to appropriate handler based on path
    if path == '/createPortfolio':
        return handle_create_portfolio(body)
    elif path == '/companyResearch':
        return handle_company_research(body)
    elif path == '/sendEmail':
        return handle_send_email(body)
    else:
        logger.warning(f"Unknown path: {path}")
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Path not found'})
        }

def handle_create_portfolio(request):
    """
    Handle request to create a portfolio
    
    Args:
        request (dict): Request data containing industry and count
        
    Returns:
        dict: Response containing portfolio data
    """
    logger.info("Handling createPortfolio request")
    
    # Extract parameters
    industry = request.get('industry', 'technology')
    count = request.get('count', 3)
    
    # Validate parameters
    if not isinstance(count, int) or count < 1 or count > 10:
        logger.warning(f"Invalid count parameter: {count}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Count must be an integer between 1 and 10'})
        }
    
    if industry not in ['technology', 'real_estate']:
        logger.warning(f"Invalid industry parameter: {industry}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Industry must be either "technology" or "real_estate"'})
        }
    
    # Get portfolio data
    portfolio_data = get_companies_by_industry(industry, count)
    
    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'success',
            'message': f'Created portfolio with {len(portfolio_data)} {industry} companies',
            'portfolio': portfolio_data
        })
    }

def handle_company_research(request):
    """
    Handle request for company research
    
    Args:
        request (dict): Request data containing ticker
        
    Returns:
        dict: Response containing company research data
    """
    logger.info("Handling companyResearch request")
    
    # Extract parameters
    ticker = request.get('ticker', '')
    
    # Validate parameters
    if not ticker:
        logger.warning("Missing ticker parameter")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Ticker parameter is required'})
        }
    
    # Get company research data
    research_data = get_company_research(ticker)
    
    if not research_data:
        logger.warning(f"Company with ticker {ticker} not found")
        return {
            'statusCode': 404,
            'body': json.dumps({'error': f'Company with ticker {ticker} not found'})
        }
    
    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'success',
            'message': f'Research retrieved for {ticker}',
            'research': research_data
        })
    }

def handle_send_email(request):
    """
    Handle request to send email
    
    Args:
        request (dict): Request data containing email details
        
    Returns:
        dict: Response containing email status
    """
    logger.info("Handling sendEmail request")
    
    # Extract parameters
    to_address = request.get('to_address', '')
    subject = request.get('subject', 'Your Portfolio')
    portfolio_data = request.get('portfolio_data', [])
    
    # Validate parameters
    if not to_address:
        logger.warning("Missing to_address parameter")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'to_address parameter is required'})
        }
    
    # Send email using SES
    result = send_email_via_ses(to_address, subject, portfolio_data)
    
    if result.get('error'):
        return {
            'statusCode': 500,
            'body': json.dumps({'error': result['error']})
        }
    
    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'success',
            'message': 'Email sent successfully',
            'messageId': result.get('messageId', '')
        })
    }

def get_companies_by_industry(industry, count):
    """
    Get top companies by industry
    
    Args:
        industry (str): Industry to filter by
        count (int): Number of companies to return
        
    Returns:
        list: List of company dictionaries
    """
    # Technology companies data
    technology_companies = [
        {
            "name": "TechCorp Inc.",
            "ticker": "TECH",
            "industry": "technology",
            "performance_score": 92,
            "market_cap": "1.2T",
            "description": "Leading provider of cloud computing services and AI solutions"
        },
        {
            "name": "Quantum Systems",
            "ticker": "QSYS",
            "industry": "technology",
            "performance_score": 88,
            "market_cap": "850B",
            "description": "Innovative semiconductor manufacturer specializing in quantum computing"
        },
        {
            "name": "DataMind Labs",
            "ticker": "DTML",
            "industry": "technology",
            "performance_score": 85,
            "market_cap": "420B",
            "description": "AI-focused research company developing cutting-edge machine learning models"
        },
        {
            "name": "Infinity Networks",
            "ticker": "INFN",
            "industry": "technology",
            "performance_score": 82,
            "market_cap": "310B",
            "description": "Global telecommunications and networking equipment provider"
        },
        {
            "name": "SecureBlock Technologies",
            "ticker": "SBLK",
            "industry": "technology",
            "performance_score": 79,
            "market_cap": "175B",
            "description": "Cybersecurity firm specializing in blockchain security solutions"
        }
    ]
    
    # Real estate companies data
    real_estate_companies = [
        {
            "name": "Urban Property Group",
            "ticker": "URPG",
            "industry": "real_estate",
            "performance_score": 89,
            "market_cap": "85B",
            "description": "Developer and manager of premium commercial properties in major urban centers"
        },
        {
            "name": "Residential REIT",
            "ticker": "RRET",
            "industry": "real_estate",
            "performance_score": 86,
            "market_cap": "62B",
            "description": "Real estate investment trust focused on multi-family residential properties"
        },
        {
            "name": "Global Logistics Properties",
            "ticker": "GLPX",
            "industry": "real_estate",
            "performance_score": 84,
            "market_cap": "58B",
            "description": "Owner and operator of logistics facilities and warehouses worldwide"
        },
        {
            "name": "Healthcare Facilities Trust",
            "ticker": "HCFT",
            "industry": "real_estate",
            "performance_score": 81,
            "market_cap": "44B",
            "description": "Specializes in medical office buildings and healthcare facilities"
        },
        {
            "name": "Digital Infrastructure REIT",
            "ticker": "DREIT",
            "industry": "real_estate",
            "performance_score": 78,
            "market_cap": "39B",
            "description": "Owns and manages data centers and digital infrastructure properties"
        }
    ]
    
    # Select companies based on industry
    if industry == 'technology':
        companies = technology_companies
    else:  # real_estate
        companies = real_estate_companies
    
    # Sort by performance score and return top count
    sorted_companies = sorted(companies, key=lambda x: x['performance_score'], reverse=True)
    return sorted_companies[:count]

def get_company_research(ticker):
    """
    Get research data for a specific company
    
    Args:
        ticker (str): Company ticker symbol
        
    Returns:
        dict: Company research data or None if not found
    """
    # Combined list of all companies
    all_companies = get_companies_by_industry('technology', 10) + get_companies_by_industry('real_estate', 10)
    
    # Find company by ticker
    for company in all_companies:
        if company['ticker'] == ticker:
            # Add additional research details
            research = {
                "ticker": ticker,
                "name": company['name'],
                "industry": company['industry'],
                "summary": company['description'],
                "performance": company['performance_score'],
                "market_cap": company['market_cap'],
                "recommendations": ["Buy" if company['performance_score'] > 85 else "Hold"],
                "risk_score": (100 - company['performance_score']) / 10,
                "growth_potential": "High" if company['performance_score'] > 85 else "Moderate",
                "analyst_consensus": "Positive" if company['performance_score'] > 80 else "Neutral"
            }
            return research
    
    # No company found with the given ticker
    return None

def send_email_via_ses(to_address, subject, portfolio_data):
    """
    Send email using AWS SES
    
    Args:
        to_address (str): Recipient email address
        subject (str): Email subject
        portfolio_data (list): Portfolio data to include in email
        
    Returns:
        dict: Result of email sending operation
    """
    # Format the email body
    body = "Here is your requested investment portfolio:\n\n"
    
    for i, company in enumerate(portfolio_data):
        body += f"{i+1}. {company.get('name', 'Unknown Company')} ({company.get('ticker', 'N/A')})\n"
        body += f"   Industry: {company.get('industry', 'Unknown')}\n"
        body += f"   Performance Score: {company.get('performance_score', 'N/A')}/100\n"
        body += f"   Market Cap: ${company.get('market_cap', 'N/A')}\n"
        body += f"   Description: {company.get('description', 'No description available')}\n\n"
    
    body += "\nThank you for using our Financial Assistant service."
    
    try:
        # Get AWS credentials from environment variables
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        sender_email = os.environ.get('SENDER_EMAIL', 'financial-assistant@example.com')
        
        # Create SES client
        ses_client = boto3.client(
            'ses',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # Send email
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [to_address]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        
        logger.info(f"Email sent via SES: {response['MessageId']}")
        return {'messageId': response['MessageId']}
        
    except ClientError as e:
        logger.error(f"Failed to send email via SES: {str(e)}")
        return {'error': str(e)}
    except Exception as e:
        logger.error(f"Unexpected error sending email via SES: {str(e)}")
        return {'error': str(e)}
