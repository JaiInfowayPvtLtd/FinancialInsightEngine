# Financial Assistant

A financial assistant that simulates Amazon Bedrock's multi-agent collaboration framework for portfolio creation and financial insights.

![Financial Assistant](generated-icon.png)

## Overview

This application demonstrates a three-agent architecture powered by Amazon Bedrock's multi-agent collaboration framework. The system includes:

1. **Supervisor Agent** - The main orchestrator that routes requests to specialized agents and manages user interaction
2. **Portfolio Assistant** - Creates portfolios of top-performing companies based on industry preferences
3. **Data Assistant** - Provides financial data insights, FOMC report summaries, and market analysis

## Features

- Create investment portfolios based on industry (Technology or Real Estate) and company count
- Receive financial insights and market trend analysis
- View summaries of Federal Open Market Committee (FOMC) reports
- Email portfolio details to users (simulated or via AWS SES)
- Interactive chat interface for natural language queries

## Tech Stack

- Python 3.11
- Streamlit for UI
- Boto3 for AWS services integration
- JSON for data storage
- OpenAPI schema for API definitions

## Project Structure

```
├── agents/                      # Agent implementation files
│   ├── supervisor.py            # Supervisor agent for orchestration
│   ├── portfolio_assistant.py   # Portfolio creation agent
│   ├── data_assistant.py        # Financial data and insights agent
├── api/                         # API definitions
│   └── openapi_schema.json      # OpenAPI schema for Lambda endpoints
├── data/                        # Data files
│   ├── companies_technology.json    # Technology companies data
│   ├── companies_real_estate.json   # Real estate companies data
│   └── fomc_summaries.json      # FOMC report summaries
├── lambda/                      # AWS Lambda functions
│   └── portfolio_assistant_lambda.py    # Lambda implementation
├── pdfs/                        # PDF files for analysis
│   └── sample_fomc_report.txt   # Sample FOMC report
├── utils/                       # Utility functions
│   ├── aws_service.py           # AWS services integration
│   ├── config.py                # Configuration settings
│   ├── email_service.py         # Email sending functionality
│   └── pdf_processor.py         # PDF processing utilities
├── .streamlit/                  # Streamlit configuration
│   └── config.toml              # Streamlit config settings
├── app.py                       # Main application entry point
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.11+
- Streamlit
- Boto3 (for AWS integration)

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install streamlit boto3
   ```
3. Run the application:
   ```
   streamlit run app.py --server.port 5000
   ```

### AWS Integration (Optional)

For full functionality with AWS services, set the following environment variables:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
USE_SES=true
SENDER_EMAIL=your-verified-email@example.com
```

## Usage

1. Open the application in your browser at http://localhost:5000
2. Enter your email address in the sidebar (optional, for portfolio delivery)
3. Use the chat interface to:
   - Create investment portfolios (e.g., "Create a portfolio of 5 technology companies")
   - Get financial insights (e.g., "Tell me about inflation trends")
   - View FOMC report summaries (e.g., "What's in the latest FOMC report?")
4. Alternatively, use the quick action buttons at the bottom of the page

## Architecture

The application simulates Amazon Bedrock's multi-agent collaboration framework with three specialized agents:

1. **Supervisor Agent**: Acts as the main orchestrator, analyzing user queries and routing them to specialized agents. It uses chain-of-thought reasoning to determine user intent and extract relevant parameters.

2. **Portfolio Assistant**: Creates portfolios of top-performing companies based on industry and company count. It can:
   - Access company data from either Lambda functions or local JSON files
   - Format portfolio information for display
   - Send portfolio details via email (simulated or using AWS SES)

3. **Data Assistant**: Provides financial insights and report summaries. It can:
   - Analyze user queries to extract key financial terms
   - Search for relevant financial insights based on these terms
   - Generate summaries of FOMC reports from stored data

## Lambda Integration

The system includes a Lambda function implementation for the Portfolio Assistant with three endpoints:
- `/createPortfolio` - Creates a portfolio based on industry and company count
- `/companyResearch` - Provides research details for a specific company by ticker
- `/sendEmail` - Sends portfolio details via email

The Lambda function is documented with an OpenAPI schema in `api/openapi_schema.json`.

## License

[MIT License](LICENSE)

## Acknowledgements

- This project simulates Amazon Bedrock capabilities locally using Python
- Data used is for demonstration purposes only