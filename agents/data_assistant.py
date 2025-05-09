import json
import logging
import os
import re
from utils.pdf_processor import PDFProcessor

class DataAssistant:
    """
    Data Assistant Agent responsible for providing financial data insights,
    FOMC report summaries, and historical company performance information
    """
    
    def __init__(self, config):
        """
        Initialize the Data Assistant
        
        Args:
            config (dict): Configuration settings for the agent
        """
        self.config = config
        self.pdf_processor = PDFProcessor()
        self.fomc_data_path = "data/fomc_summaries.json"
        self.sample_fomc_path = "pdfs/sample_fomc_report.txt"
        logging.info("Data Assistant initialized")
    
    def get_financial_insights(self, query):
        """
        Provide financial data insights based on user query
        
        Args:
            query (str): The user's query
            
        Returns:
            str: Financial insights relevant to the query
        """
        logging.info(f"Getting financial insights for query: {query}")
        
        # Extract key terms from the query
        key_terms = self._extract_key_terms(query)
        logging.info(f"Extracted key terms: {key_terms}")
        
        # Get relevant insights based on key terms
        insights = self._search_financial_insights(key_terms)
        
        if not insights:
            return (
                "I don't have specific financial insights matching your query at the moment. "
                "You can ask about market trends, industry performance, or FOMC reports."
            )
        
        # Format the response
        response = "📈 **Financial Insights**\n\n"
        for insight in insights:
            response += f"**{insight['title']}**\n{insight['content']}\n\n"
        
        response += "Would you like to know more about any particular aspect?"
        return response
    
    def get_fomc_summary(self):
        """
        Provide a summary of the latest FOMC report
        
        Returns:
            str: FOMC report summary
        """
        logging.info("Getting FOMC report summary")
        
        try:
            # First try to load from JSON file
            with open(self.fomc_data_path, 'r') as f:
                fomc_data = json.load(f)
                latest_report = fomc_data[-1]  # Assume last entry is the latest
                
                response = (
                    f"📝 **FOMC Report Summary ({latest_report.get('date', 'Recent Meeting')})**\n\n"
                    f"{latest_report.get('summary', 'Summary not available.')}\n\n"
                    f"**Key Points:**\n"
                )
                
                for point in latest_report.get('key_points', []):
                    response += f"- {point}\n"
                
                return response
                
        except (FileNotFoundError, json.JSONDecodeError, IndexError) as e:
            logging.warning(f"Error loading FOMC data from JSON: {str(e)}. Falling back to sample report.")
            
            # Fallback: Extract from sample FOMC report text file
            try:
                fomc_text = self._load_sample_fomc_report()
                summary = self._generate_fomc_summary(fomc_text)
                return summary
                
            except Exception as pdf_error:
                logging.error(f"Error processing sample FOMC report: {str(pdf_error)}")
                return "I'm unable to retrieve the FOMC report summary at this time. Please try again later."
    
    def _extract_key_terms(self, query):
        """
        Extract key financial terms from the user query
        
        Args:
            query (str): The user's query
            
        Returns:
            list: List of key financial terms
        """
        # List of common financial terms to look for
        financial_terms = [
            "inflation", "interest rates", "gdp", "growth", "recession",
            "market", "stock", "bond", "yield", "investment", "economy",
            "sector", "industry", "performance", "trends", "forecast"
        ]
        
        # Extract terms that appear in the query
        extracted_terms = []
        query_lower = query.lower()
        
        for term in financial_terms:
            if term in query_lower:
                extracted_terms.append(term)
        
        # Extract company names or tickers (simplified)
        ticker_pattern = r'\b[A-Z]{1,5}\b'  # Simple pattern for stock tickers
        tickers = re.findall(ticker_pattern, query)
        extracted_terms.extend(tickers)
        
        return extracted_terms
    
    def _search_financial_insights(self, key_terms):
        """
        Search for financial insights related to key terms
        
        Args:
            key_terms (list): List of key financial terms
            
        Returns:
            list: List of relevant financial insights
        """
        # Define some static financial insights for common terms
        insights_database = {
            "inflation": {
                "title": "Inflation Trends",
                "content": "Recent data shows inflation has moderated from previous highs, but remains above the Federal Reserve's target of 2%. Core inflation, which excludes food and energy, has been particularly persistent in service sectors."
            },
            "interest rates": {
                "title": "Interest Rate Environment",
                "content": "The Federal Reserve has maintained elevated interest rates to combat inflation. Markets are currently anticipating potential rate cuts in the coming quarters as inflation pressures ease, though the timing remains uncertain."
            },
            "market": {
                "title": "Market Performance",
                "content": "Equity markets have shown resilience despite higher interest rates, with technology stocks demonstrating particular strength. Fixed income markets have adjusted to the higher rate environment with yields stabilizing."
            },
            "economy": {
                "title": "Economic Outlook",
                "content": "The economy has maintained growth despite tighter monetary conditions. Consumer spending remains relatively strong, though there are signs of moderation in certain sectors. The labor market has shown cooling but remains historically tight."
            },
            "technology": {
                "title": "Technology Sector Insights",
                "content": "The technology sector continues to outperform broader markets, driven by advances in artificial intelligence, cloud computing, and digital transformation. Companies with strong AI capabilities have seen particularly robust valuations."
            },
            "real estate": {
                "title": "Real Estate Market Conditions",
                "content": "The real estate sector has faced challenges from higher interest rates, particularly in residential and commercial segments. REITs have experienced pressure, though certain subsectors like data centers and industrial properties have shown resilience."
            }
        }
        
        # Collect insights relevant to the key terms
        relevant_insights = []
        for term in key_terms:
            if term.lower() in insights_database:
                relevant_insights.append(insights_database[term.lower()])
        
        return relevant_insights
    
    def _load_sample_fomc_report(self):
        """
        Load sample FOMC report text
        
        Returns:
            str: Text content of the sample FOMC report
        """
        try:
            with open(self.sample_fomc_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logging.error(f"Sample FOMC report file not found: {self.sample_fomc_path}")
            # Return a minimal sample text if file not found
            return (
                "Federal Reserve issues FOMC statement. "
                "The Committee decided to maintain the target range for the federal funds rate. "
                "Recent indicators suggest that economic activity has continued to expand at a moderate pace. "
                "Inflation remains elevated."
            )
    
    def _generate_fomc_summary(self, fomc_text):
        """
        Generate a summary from FOMC report text
        
        Args:
            fomc_text (str): Text content of FOMC report
            
        Returns:
            str: Formatted FOMC summary
        """
        # This is a simplified summary generation
        # In a real system, this would use more sophisticated NLP
        
        # Extract key sections (simplified)
        monetary_policy = "The Committee decided to maintain the target range for the federal funds rate."
        economic_assessment = "Recent indicators suggest that economic activity has continued to expand at a moderate pace."
        inflation_outlook = "Inflation remains elevated but has shown signs of moderation in recent months."
        
        # Generate key points
        key_points = [
            "The Federal Reserve maintains its commitment to achieving maximum employment and inflation at the rate of 2 percent over the longer run.",
            "The Committee will continue to monitor the implications of incoming information for the economic outlook.",
            "The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge.",
            "The Committee's assessments will take into account a wide range of information, including labor market conditions, inflation pressures, and financial and international developments."
        ]
        
        # Format the response
        response = (
            f"📝 **FOMC Report Summary (Recent Meeting)**\n\n"
            f"The Federal Open Market Committee (FOMC) has released its latest policy statement. {monetary_policy} "
            f"{economic_assessment} {inflation_outlook}\n\n"
            f"**Key Points:**\n"
        )
        
        for point in key_points:
            response += f"- {point}\n"
        
        return response
