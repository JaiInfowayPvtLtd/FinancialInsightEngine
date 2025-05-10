# Financial Assistant User Guide

This user guide explains how to use the Financial Assistant application to get investment portfolio recommendations, financial insights, and FOMC report summaries.

## Getting Started

1. Launch the application by running the command: `streamlit run app.py --server.port 5000`
2. Access the application through your web browser at: http://localhost:5000
3. The application interface is divided into these main sections:
   - Header with app title and description
   - Sidebar for user information
   - Chat interface for queries and responses
   - Quick action buttons for common requests

## User Information

In the sidebar, you can provide your email address if you'd like to receive portfolio recommendations via email. This is optional but recommended if you want to save your portfolio information.

## Asking Questions

### Using the Chat Interface

You can interact with the Financial Assistant by typing your questions in the text area and clicking the "Send" button. Here are examples of queries you can ask:

1. **Portfolio Creation**
   - "Create a portfolio of 5 technology companies"
   - "I want a portfolio with 3 real estate companies"
   - "Show me the top technology stocks for investment"

2. **Financial Insights**
   - "Tell me about current inflation trends"
   - "What's happening with interest rates?"
   - "Provide insights on the technology sector"

3. **FOMC Report Information**
   - "What's in the latest FOMC report?"
   - "Summarize the most recent Federal Reserve meeting"
   - "Tell me about the Fed's current policy stance"

### Using Quick Action Buttons

For common requests, you can use the quick action buttons at the bottom of the screen:

- **Create Tech Portfolio**: Automatically creates a portfolio of 3 top technology companies
- **Create Real Estate Portfolio**: Automatically creates a portfolio of 3 top real estate companies
- **Latest FOMC Summary**: Provides a summary of the most recent Federal Open Market Committee report

## Understanding Responses

### Portfolio Recommendations

When you request a portfolio, the response will include:
- A header indicating the industry and number of companies
- A list of recommended companies with their ticker symbols
- Performance scores (out of 100) for each company
- Market capitalization information
- Email status (if you provided an email address)

Example:
```
📊 Portfolio Created: Top 3 Technology Companies

1. TechCorp Inc. (TECH)
   Industry: technology
   Performance Score: 92/100
   Market Cap: $1.2T

2. Quantum Systems (QSYS)
   Industry: technology
   Performance Score: 88/100
   Market Cap: $850B

3. DataMind Labs (DTML)
   Industry: technology
   Performance Score: 85/100
   Market Cap: $420B

Email Status: Portfolio has been emailed to you successfully.

Would you like me to provide more details about any of these companies?
```

### Financial Insights

Financial insight responses include:
- A header indicating the type of insight
- Detailed information about the requested financial topic
- Current trends and analysis

Example:
```
📈 Financial Insights

Inflation Trends
Recent data shows inflation has moderated from previous highs, but remains above the Federal Reserve's target of 2%. Core inflation, which excludes food and energy, has been particularly persistent in service sectors.

Would you like to know more about any particular aspect?
```

### FOMC Report Summaries

FOMC report summaries include:
- The date of the FOMC meeting
- A summary of the report's main points
- Key decisions and policy actions
- Economic assessments

Example:
```
📝 FOMC Report Summary (May 1, 2024)

The Federal Open Market Committee (FOMC) has released its latest policy statement. The Committee decided to maintain the target range for the federal funds rate at 5-1/4 to 5-1/2 percent. Recent indicators suggest that economic activity has continued to expand at a moderate pace. Inflation remains elevated but has shown signs of moderation in recent months.

Key Points:
- The Federal Reserve maintains its commitment to achieving maximum employment and inflation at the rate of 2 percent over the longer run.
- The Committee will continue to monitor the implications of incoming information for the economic outlook.
- The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge.
- The Committee's assessments will take into account a wide range of information, including labor market conditions, inflation pressures, and financial and international developments.
```

## Email Delivery

If you provide your email address in the sidebar, portfolio recommendations can be sent to your email. The email will contain:
- A formatted list of the recommended companies
- Performance scores and market capitalization information
- Brief descriptions of each company

## Tips for Best Results

1. **Be specific in your requests**: Mention the industry and number of companies you're interested in for portfolio creation
2. **Use natural language**: The assistant understands conversational language, so you can ask questions as you would to a human financial advisor
3. **Ask follow-up questions**: After receiving a response, you can ask for more details or clarification on specific points
4. **Explore different industries**: The system currently supports technology and real estate portfolios
5. **Check FOMC updates**: The FOMC data is updated regularly, so check back for the latest information