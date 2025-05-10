# Financial Assistant API Documentation

This document details the API endpoints implemented in the Portfolio Assistant Lambda function. These endpoints allow for portfolio creation, company research, and email delivery.

## Base URL

For local development and testing:
```
http://localhost:8000
```

## Authentication

The API does not currently implement authentication. In a production environment, you would need to implement appropriate authentication methods (e.g., API keys, IAM roles, or OAuth tokens).

## Endpoints

### 1. Create Portfolio

Creates a portfolio of top-performing companies based on industry and count.

**Endpoint:** `/createPortfolio`

**Method:** POST

**Request Body:**
```json
{
  "industry": "technology",
  "count": 3
}
```

**Parameters:**
- `industry` (string, required): The industry to focus on. Valid values are "technology" or "real_estate".
- `count` (integer, required): Number of companies to include in the portfolio. Must be between 1 and 10.

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Created portfolio with 3 technology companies",
  "portfolio": [
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
    }
  ]
}
```

**Error Responses:**

- 400 Bad Request - If the parameters are invalid
```json
{
  "error": "Industry must be either 'technology' or 'real_estate'"
}
```

- 400 Bad Request - If the count is out of range
```json
{
  "error": "Count must be an integer between 1 and 10"
}
```

### 2. Company Research

Retrieves detailed research information for a specific company by ticker symbol.

**Endpoint:** `/companyResearch`

**Method:** POST

**Request Body:**
```json
{
  "ticker": "TECH"
}
```

**Parameters:**
- `ticker` (string, required): The ticker symbol of the company to research.

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Research retrieved for TECH",
  "research": {
    "ticker": "TECH",
    "name": "TechCorp Inc.",
    "industry": "technology",
    "summary": "Leading provider of cloud computing services and AI solutions",
    "performance": 92,
    "market_cap": "1.2T",
    "recommendations": ["Buy"],
    "risk_score": 0.8,
    "growth_potential": "High",
    "analyst_consensus": "Positive"
  }
}
```

**Error Responses:**

- 400 Bad Request - If the ticker parameter is missing
```json
{
  "error": "Ticker parameter is required"
}
```

- 404 Not Found - If the company with the specified ticker is not found
```json
{
  "error": "Company with ticker UNKNOWN not found"
}
```

### 3. Send Email

Sends portfolio details to a specified email address.

**Endpoint:** `/sendEmail`

**Method:** POST

**Request Body:**
```json
{
  "to_address": "user@example.com",
  "subject": "Your Technology Portfolio",
  "portfolio_data": [
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
    }
  ]
}
```

**Parameters:**
- `to_address` (string, required): The email address to send the portfolio to.
- `subject` (string, optional): The email subject line. Default is "Your Portfolio".
- `portfolio_data` (array, required): An array of company objects to include in the email.

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Email sent successfully",
  "messageId": "0102018abc-123a-4567-89bc-def012345678-000000"
}
```

**Error Responses:**

- 400 Bad Request - If the email address is missing
```json
{
  "error": "to_address parameter is required"
}
```

- 500 Internal Server Error - If email sending fails
```json
{
  "error": "Failed to send email: [error details]"
}
```

## Data Models

### Company Information Object

```json
{
  "name": "String",
  "ticker": "String",
  "industry": "String",
  "performance_score": "Integer",
  "market_cap": "String",
  "description": "String"
}
```

### Company Research Object

```json
{
  "ticker": "String",
  "name": "String",
  "industry": "String",
  "summary": "String",
  "performance": "Integer",
  "market_cap": "String",
  "recommendations": ["String"],
  "risk_score": "Float",
  "growth_potential": "String",
  "analyst_consensus": "String"
}
```

## Error Handling

All API endpoints follow a consistent error response format:

```json
{
  "error": "Description of the error"
}
```

Error responses include appropriate HTTP status codes:
- 400: Bad Request - Invalid parameters
- 404: Not Found - Resource not found
- 500: Internal Server Error - Server-side issues

## Testing the API

You can test the API using curl:

### Create Portfolio
```bash
curl -X POST http://localhost:8000/createPortfolio \
  -H "Content-Type: application/json" \
  -d '{"industry": "technology", "count": 3}'
```

### Company Research
```bash
curl -X POST http://localhost:8000/companyResearch \
  -H "Content-Type: application/json" \
  -d '{"ticker": "TECH"}'
```

### Send Email
```bash
curl -X POST http://localhost:8000/sendEmail \
  -H "Content-Type: application/json" \
  -d '{
    "to_address": "user@example.com",
    "subject": "Your Technology Portfolio",
    "portfolio_data": [
      {
        "name": "TechCorp Inc.",
        "ticker": "TECH",
        "industry": "technology",
        "performance_score": 92,
        "market_cap": "1.2T"
      }
    ]
  }'
```

## Implementation Notes

The API is implemented as an AWS Lambda function in `lambda/portfolio_assistant_lambda.py`. For local development and testing, you can use AWS SAM or a tool like Lambda Local to run the function locally.

For AWS deployment, you would need to:
1. Package the Lambda function
2. Deploy to AWS Lambda
3. Configure an API Gateway to expose the endpoints
4. Set up appropriate IAM roles for the Lambda function to use AWS SES for email sending

The complete API schema is available in OpenAPI format at `api/openapi_schema.json`.