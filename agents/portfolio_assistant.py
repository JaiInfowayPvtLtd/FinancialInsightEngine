import json
import logging
import os
import requests
from utils.email_service import EmailService

class PortfolioAssistant:
    """
    Portfolio Assistant Agent responsible for creating portfolios
    and sending them via email
    """
    
    def __init__(self, config):
        """
        Initialize the Portfolio Assistant with configuration
        
        Args:
            config (dict): Configuration settings for the agent
        """
        self.config = config
        self.email_service = EmailService(config)
        self.lambda_base_url = self.config.get('lambda_base_url', 'http://localhost:8000')
        logging.info("Portfolio Assistant initialized")
    
    def create_portfolio(self, industry, company_count=3, user_email=None):
        """
        Create a portfolio of top companies based on industry and count
        
        Args:
            industry (str): The industry to focus on ('technology' or 'real_estate')
            company_count (int): Number of companies to include
            user_email (str, optional): User's email for sending portfolio
            
        Returns:
            str: A formatted response with the created portfolio
        """
        logging.info(f"Creating portfolio for industry: {industry}, count: {company_count}")
        
        # First, try to use the Lambda function
        try:
            lambda_response = self._call_lambda_endpoint(
                endpoint="/createPortfolio",
                payload={
                    "industry": industry,
                    "count": company_count
                }
            )
            
            # If Lambda call successful, use its response
            portfolio_data = lambda_response.get('portfolio', [])
            logging.info(f"Successfully retrieved portfolio from Lambda with {len(portfolio_data)} companies")
            
        except Exception as e:
            logging.warning(f"Lambda call failed: {str(e)}. Falling back to local data.")
            
            # Lambda call failed, use local data as fallback
            portfolio_data = self._get_companies_from_local_data(industry, company_count)
            logging.info(f"Retrieved {len(portfolio_data)} companies from local data")
        
        # Format the portfolio for display
        formatted_portfolio = self._format_portfolio(portfolio_data)
        
        # Send email if user provided an email address
        email_status = "Email delivery was not requested."
        if user_email:
            email_status = self._send_portfolio_email(user_email, industry, portfolio_data)
        
        # Compose the full response
        response = (
            f"📊 **Portfolio Created: Top {company_count} {industry.replace('_', ' ').title()} Companies**\n\n"
            f"{formatted_portfolio}\n\n"
            f"**Email Status**: {email_status}\n\n"
            f"Would you like me to provide more details about any of these companies?"
        )
        
        return response
    
    def _get_companies_from_local_data(self, industry, count):
        """
        Get companies from local data files
        
        Args:
            industry (str): The industry to focus on ('technology' or 'real_estate')
            count (int): Number of companies to include
            
        Returns:
            list: List of company dictionaries
        """
        # Map industry to file path
        industry_files = {
            'technology': 'data/companies_technology.json',
            'real_estate': 'data/companies_real_estate.json'
        }
        
        # Normalize industry name
        normalized_industry = industry.lower().replace(' ', '_')
        file_path = industry_files.get(normalized_industry, industry_files['technology'])
        
        try:
            with open(file_path, 'r') as f:
                companies = json.load(f)
                
            # Sort companies by performance score and take the top ones
            sorted_companies = sorted(companies, key=lambda x: x.get('performance_score', 0), reverse=True)
            return sorted_companies[:count]
            
        except FileNotFoundError:
            logging.error(f"Companies data file not found: {file_path}")
            # Return sample data if file not found
            return [
                {"name": "Example Corp", "ticker": "EX", "industry": industry, "performance_score": 85}
            ]
    
    def _call_lambda_endpoint(self, endpoint, payload):
        """
        Call a Lambda function endpoint
        
        Args:
            endpoint (str): The endpoint path
            payload (dict): The payload to send
            
        Returns:
            dict: The response from the Lambda function
        """
        url = f"{self.lambda_base_url}{endpoint}"
        
        # Simulate API call to Lambda function
        try:
            # For simulation purposes, we're not actually making an HTTP request
            # This would be replaced with a real HTTP request in production
            if endpoint == "/createPortfolio":
                return self._simulate_lambda_portfolio_response(payload)
            elif endpoint == "/companyResearch":
                return self._simulate_lambda_research_response(payload)
            elif endpoint == "/sendEmail":
                return self._simulate_lambda_email_response(payload)
            else:
                raise ValueError(f"Unknown endpoint: {endpoint}")
                
        except Exception as e:
            logging.error(f"Error calling Lambda endpoint {endpoint}: {str(e)}")
            raise
    
    def _simulate_lambda_portfolio_response(self, payload):
        """Simulate a response from the Lambda portfolio endpoint"""
        industry = payload.get("industry", "technology")
        count = payload.get("count", 3)
        
        # Get companies from local data (the same way as the fallback mechanism)
        companies = self._get_companies_from_local_data(industry, count)
        
        return {
            "status": "success",
            "message": f"Created portfolio with {len(companies)} {industry} companies",
            "portfolio": companies
        }
    
    def _simulate_lambda_research_response(self, payload):
        """Simulate a response from the Lambda research endpoint"""
        ticker = payload.get("ticker", "")
        
        return {
            "status": "success",
            "message": f"Research retrieved for {ticker}",
            "research": {
                "ticker": ticker,
                "summary": f"This is a simulated research summary for {ticker}.",
                "recommendations": ["Buy", "Hold"],
                "risk_score": 7.5
            }
        }
    
    def _simulate_lambda_email_response(self, payload):
        """Simulate a response from the Lambda email endpoint"""
        return {
            "status": "success",
            "message": "Email sent successfully"
        }
    
    def _format_portfolio(self, portfolio_data):
        """
        Format portfolio data for display
        
        Args:
            portfolio_data (list): List of company dictionaries
            
        Returns:
            str: Formatted portfolio text
        """
        if not portfolio_data:
            return "No companies found for this portfolio."
        
        formatted_text = ""
        for i, company in enumerate(portfolio_data):
            formatted_text += (
                f"{i+1}. **{company.get('name', 'Unknown Company')}** ({company.get('ticker', 'N/A')})\n"
                f"   Industry: {company.get('industry', 'Unknown')}\n"
                f"   Performance Score: {company.get('performance_score', 'N/A')}/100\n"
                f"   Market Cap: ${company.get('market_cap', 'N/A')}\n\n"
            )
        
        return formatted_text
    
    def _send_portfolio_email(self, user_email, industry, portfolio_data):
        """
        Send portfolio to user via email
        
        Args:
            user_email (str): User's email address
            industry (str): The industry of the portfolio
            portfolio_data (list): List of company dictionaries
            
        Returns:
            str: Status message about email delivery
        """
        if not user_email:
            return "No email address provided."
        
        try:
            # First try using the Lambda function
            email_payload = {
                "to_address": user_email,
                "subject": f"Your {industry.replace('_', ' ').title()} Portfolio",
                "portfolio_data": portfolio_data
            }
            
            lambda_response = self._call_lambda_endpoint(
                endpoint="/sendEmail",
                payload=email_payload
            )
            
            return "Portfolio has been emailed to you successfully."
            
        except Exception as e:
            logging.warning(f"Lambda email sending failed: {str(e)}. Falling back to local email service.")
            
            # Try using the local email service as fallback
            try:
                subject = f"Your {industry.replace('_', ' ').title()} Portfolio"
                body = f"Here is your requested portfolio of top {industry.replace('_', ' ')} companies:\n\n"
                body += self._format_portfolio(portfolio_data)
                
                self.email_service.send_email(
                    to_address=user_email,
                    subject=subject,
                    body=body
                )
                
                return "Portfolio has been emailed to you successfully."
                
            except Exception as email_error:
                logging.error(f"Email sending failed: {str(email_error)}")
                return "Unable to send email at this time. Please try again later."
