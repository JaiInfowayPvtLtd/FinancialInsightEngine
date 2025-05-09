import json
import logging
from agents.portfolio_assistant import PortfolioAssistant
from agents.data_assistant import DataAssistant

class SupervisorAgent:
    """
    The Supervisor Agent acts as the main orchestrator.
    It routes requests to specialized agents and manages user interaction.
    """
    
    def __init__(self, config):
        """
        Initialize the supervisor agent with configuration and sub-agents
        
        Args:
            config (dict): Configuration settings for the agent
        """
        self.config = config
        self.portfolio_assistant = PortfolioAssistant(config)
        self.data_assistant = DataAssistant(config)
        logging.info("Supervisor Agent initialized")
    
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
        
        # Analyze the query using chain-of-thought reasoning
        query_analysis = self._analyze_query(user_query)
        request_type = query_analysis['request_type']
        
        # Route to appropriate agent based on request type
        if request_type == 'portfolio_creation':
            # Extract parameters for portfolio creation
            params = self._extract_portfolio_params(user_query)
            logging.info(f"Routing to Portfolio Assistant with params: {params}")
            response = self.portfolio_assistant.create_portfolio(
                industry=params['industry'],
                company_count=params['company_count'],
                user_email=user_email
            )
            return response
        
        elif request_type == 'financial_data':
            logging.info("Routing to Data Assistant for financial data")
            response = self.data_assistant.get_financial_insights(user_query)
            return response
        
        elif request_type == 'fomc_summary':
            logging.info("Routing to Data Assistant for FOMC summary")
            response = self.data_assistant.get_fomc_summary()
            return response
        
        else:
            # Handle general queries or provide help
            return self._general_response(user_query)
    
    def _analyze_query(self, query):
        """
        Analyze the user query to determine the intent
        
        Args:
            query (str): The user's query text
            
        Returns:
            dict: Analysis results including request type
        """
        query = query.lower()
        
        # Portfolio creation keywords
        portfolio_keywords = ['portfolio', 'create', 'investment', 'companies', 'stocks']
        # Financial data keywords
        data_keywords = ['data', 'financial', 'performance', 'stats', 'statistics']
        # FOMC report keywords
        fomc_keywords = ['fomc', 'federal reserve', 'report', 'fed', 'summary']
        
        # Count keyword matches for each category
        portfolio_count = sum(1 for keyword in portfolio_keywords if keyword in query)
        data_count = sum(1 for keyword in data_keywords if keyword in query)
        fomc_count = sum(1 for keyword in fomc_keywords if keyword in query)
        
        # Determine request type based on keyword matches
        if portfolio_count > max(data_count, fomc_count):
            return {'request_type': 'portfolio_creation'}
        elif fomc_count > max(portfolio_count, data_count):
            return {'request_type': 'fomc_summary'}
        elif data_count > max(portfolio_count, fomc_count):
            return {'request_type': 'financial_data'}
        else:
            return {'request_type': 'general'}
    
    def _extract_portfolio_params(self, query):
        """
        Extract portfolio creation parameters from the query
        
        Args:
            query (str): The user's query text
            
        Returns:
            dict: Extracted parameters for portfolio creation
        """
        query = query.lower()
        
        # Default values
        params = {
            'industry': 'technology',  # Default industry
            'company_count': 3  # Default number of companies
        }
        
        # Extract industry
        if 'tech' in query or 'technology' in query:
            params['industry'] = 'technology'
        elif 'real estate' in query or 'property' in query:
            params['industry'] = 'real_estate'
        
        # Extract company count
        import re
        count_matches = re.findall(r'(\d+)\s+(?:companies|company|stocks)', query)
        if count_matches:
            params['company_count'] = int(count_matches[0])
        
        return params
    
    def _general_response(self, query):
        """
        Generate a general response for queries that don't match specific intents
        
        Args:
            query (str): The user's query text
            
        Returns:
            str: General response message
        """
        return (
            "I'm your financial assistant, and I can help with:\n\n"
            "1. Creating investment portfolios (e.g., 'Create a portfolio of 5 technology companies')\n"
            "2. Providing financial insights (e.g., 'Tell me about financial performance trends')\n"
            "3. Summarizing FOMC reports (e.g., 'What's in the latest FOMC report?')\n\n"
            "Please let me know how I can assist you with these topics!"
        )
