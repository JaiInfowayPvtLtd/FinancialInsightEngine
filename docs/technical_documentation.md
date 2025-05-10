# Financial Assistant Technical Documentation

This document provides detailed technical information about the Financial Assistant application, its architecture, components, and implementation details.

## System Architecture

The Financial Assistant is built on a multi-agent architecture inspired by Amazon Bedrock's agent collaboration framework, consisting of three primary agents:

1. **Supervisor Agent** - Orchestrates the system and routes user requests
2. **Portfolio Assistant** - Handles portfolio creation and email delivery
3. **Data Assistant** - Provides financial insights and FOMC report summaries

### Architecture Diagram

```
┌─────────────────┐                       ┌───────────────────────┐
│                 │                       │                       │
│     User UI     │◄────────────────────►│    Supervisor Agent   │
│  (Streamlit)    │                       │                       │
│                 │                       └───────────┬───────────┘
└─────────────────┘                                   │
                                                      │
                                         ┌────────────┴────────────┐
                                         │                         │
                             ┌───────────┴──────────┐   ┌─────────┴──────────┐
                             │                      │   │                    │
                             │ Portfolio Assistant  │   │   Data Assistant   │
                             │                      │   │                    │
                             └──────────┬───────────┘   └──────────┬─────────┘
                                        │                          │
                                        │                          │
                             ┌──────────┴───────────┐   ┌──────────┴─────────┐
                             │                      │   │                    │
                             │   Lambda Function    │   │   Financial Data   │
                             │   (AWS SES Email)    │   │   FOMC Reports     │
                             │                      │   │                    │
                             └──────────────────────┘   └────────────────────┘
```

## Component Details

### 1. Supervisor Agent (`agents/supervisor.py`)

The Supervisor Agent is the main entry point for user requests and is responsible for:

- Analyzing user queries using chain-of-thought reasoning
- Determining the intent of the user's request
- Routing to the appropriate specialized agent
- Extracting parameters from natural language queries
- Providing general responses for unmatched queries

Key methods:
- `process_request(user_query, user_email)`: Main method for handling user requests
- `_analyze_query(query)`: Determines request type based on keyword analysis
- `_extract_portfolio_params(query)`: Extracts industry and company count from portfolio requests

### 2. Portfolio Assistant (`agents/portfolio_assistant.py`)

The Portfolio Assistant is responsible for:

- Creating portfolios based on industry and company count
- Fetching company data from either Lambda functions or local files
- Formatting portfolio data for display
- Sending portfolio information via email

Key methods:
- `create_portfolio(industry, company_count, user_email)`: Main method for portfolio creation
- `_get_companies_from_local_data(industry, count)`: Retrieves company data from JSON files
- `_call_lambda_endpoint(endpoint, payload)`: Calls Lambda function endpoints
- `_send_portfolio_email(user_email, industry, portfolio_data)`: Sends portfolio via email

### 3. Data Assistant (`agents/data_assistant.py`)

The Data Assistant is responsible for:

- Providing financial insights based on user queries
- Generating summaries of FOMC reports
- Extracting key terms from user queries
- Searching for relevant financial information

Key methods:
- `get_financial_insights(query)`: Main method for providing financial information
- `get_fomc_summary()`: Retrieves and formats FOMC report summaries
- `_extract_key_terms(query)`: Identifies financial terms in user queries
- `_search_financial_insights(key_terms)`: Finds relevant insights for key terms

### 4. Lambda Function (`lambda/portfolio_assistant_lambda.py`)

The Lambda function implementation includes three endpoints:

- `/createPortfolio`: Creates a portfolio based on industry and count
- `/companyResearch`: Provides research for a specific company by ticker
- `/sendEmail`: Sends portfolio details via email

The Lambda function is defined with an OpenAPI schema in `api/openapi_schema.json`.

### 5. Utility Services

#### AWS Service (`utils/aws_service.py`)
Handles AWS service integration, including:
- Bedrock agent invocation
- Lambda function calls
- Simulation of responses for development

#### Email Service (`utils/email_service.py`)
Manages email sending functionality:
- AWS SES integration for production
- Simulated email sending for development

#### PDF Processor (`utils/pdf_processor.py`)
Processes PDF files for data extraction:
- Text extraction
- Term searching
- Summarization

#### Configuration (`utils/config.py`)
Manages application configuration:
- Environment variable loading
- Default configuration settings
- Logging setup

## Data Storage

### JSON Data Files

- `data/companies_technology.json`: Contains information about technology companies
- `data/companies_real_estate.json`: Contains information about real estate companies
- `data/fomc_summaries.json`: Contains summaries of FOMC reports

### Sample Data Structure

#### Company Data
```json
{
  "name": "TechCorp Inc.",
  "ticker": "TECH",
  "industry": "technology",
  "performance_score": 92,
  "market_cap": "1.2T",
  "description": "Leading provider of cloud computing services and AI solutions"
}
```

#### FOMC Report Data
```json
{
  "date": "May 1, 2024",
  "summary": "The Federal Open Market Committee (FOMC) decided to maintain the target range...",
  "key_points": [
    "The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run.",
    "..."
  ],
  "policy_actions": "Maintain the target range for the federal funds rate at 5-1/4 to 5-1/2 percent",
  "economic_assessment": "Economic activity has continued to expand at a moderate pace; inflation has eased but remains elevated."
}
```

## User Interface

The user interface is built with Streamlit and includes:

- A header with application title and description
- A sidebar for user information (email address)
- A chat interface for user queries and assistant responses
- Quick action buttons for common requests

The UI is implemented in `app.py` and is configured with the settings in `.streamlit/config.toml`.

## Workflow

1. User submits a query through the Streamlit interface
2. Query is sent to the Supervisor Agent for analysis
3. Supervisor determines the intent and extracts parameters
4. Request is routed to the appropriate specialized agent
5. Specialized agent processes the request and returns a response
6. Response is displayed to the user in the chat interface
7. Chat history is stored in the Streamlit session state

## AWS Integration

The application can integrate with AWS services:

- **Amazon Bedrock**: For agent orchestration (simulated locally)
- **AWS Lambda**: For portfolio assistant functionality
- **Amazon SES**: For email delivery
- **Amazon S3**: For storing PDF files (simulated locally)

AWS integration is optional and can be enabled by setting the appropriate environment variables.

## Error Handling

The application includes comprehensive error handling:

- Fallback to local data if Lambda calls fail
- Graceful degradation for email delivery failures
- Simulated responses for development when AWS services are unavailable
- Descriptive error messages for invalid user inputs

## Logging

The application uses Python's `logging` module with configurable log levels:

- Initialization of components
- User request processing
- API calls and responses
- Error conditions

The log level can be configured using the `LOG_LEVEL` environment variable.

## Security Considerations

- AWS credentials are loaded from environment variables
- Email addresses are validated before use
- API endpoints include input validation
- External service calls are wrapped in try-except blocks

## Extension Points

The application can be extended in several ways:

1. **Additional Agents**: New specialized agents can be added by implementing the agent interface
2. **Real-time Data**: Integration with financial data APIs for real-time information
3. **User Authentication**: Adding user accounts and personalized recommendations
4. **Additional Industries**: Expanding portfolio creation to more industries
5. **Natural Language Processing**: Enhancing query understanding with more advanced NLP