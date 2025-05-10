# Financial Assistant Deployment Guide

This guide covers how to deploy the Financial Assistant application in various environments, from local development to production deployment on AWS.

## Local Deployment

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### Steps

1. **Clone or download the repository**

   ```bash
   git clone https://github.com/yourusername/financial-assistant.git
   cd financial-assistant
   ```

2. **Install the required dependencies**

   ```bash
   pip install streamlit boto3
   ```

3. **Set up environment variables (optional)**

   For local testing without AWS services, no environment variables are required. The application will use simulated responses.

   If you want to test with AWS services:

   ```bash
   # For Linux/macOS
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=us-east-1
   export USE_SES=true
   export SENDER_EMAIL=your-verified-email@example.com

   # For Windows
   set AWS_ACCESS_KEY_ID=your_access_key
   set AWS_SECRET_ACCESS_KEY=your_secret_key
   set AWS_REGION=us-east-1
   set USE_SES=true
   set SENDER_EMAIL=your-verified-email@example.com
   ```

4. **Run the application**

   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Access the application**

   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Deploying with Streamlit Sharing

Streamlit Sharing is a free service that allows you to deploy Streamlit apps directly from GitHub.

### Prerequisites

- GitHub account
- Repository containing your Financial Assistant code
- Streamlit Sharing account (sign up at https://streamlit.io/sharing)

### Steps

1. **Push your code to GitHub**

   Create a GitHub repository and push your code:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/financial-assistant.git
   git push -u origin main
   ```

2. **Deploy using Streamlit Sharing**

   - Log in to Streamlit Sharing
   - Click "New app"
   - Enter your GitHub repository details
   - Set the main file path to "app.py"
   - Click "Deploy"

3. **Set up secrets (environment variables)**

   In the Streamlit Sharing dashboard:
   - Navigate to your app
   - Click "Settings" > "Secrets"
   - Add your AWS credentials and other configuration values

## AWS Deployment

For a production deployment on AWS, you'll need to deploy both the Streamlit web application and the Lambda functions.

### Prerequisites

- AWS account
- AWS CLI installed and configured
- IAM user with appropriate permissions
- Amazon SES verified sender email (for email functionality)

### Deploying the Lambda Function

1. **Prepare the Lambda function code**

   Create a deployment package:

   ```bash
   cd lambda
   pip install -t ./package boto3
   cd package
   zip -r ../lambda_function.zip .
   cd ..
   zip -g lambda_function.zip portfolio_assistant_lambda.py
   ```

2. **Create an IAM role for the Lambda function**

   Create a role with:
   - AWSLambdaBasicExecutionRole
   - AmazonSESFullAccess (for email functionality)

3. **Create the Lambda function**

   ```bash
   aws lambda create-function \
     --function-name portfolio-assistant \
     --zip-file fileb://lambda_function.zip \
     --handler portfolio_assistant_lambda.lambda_handler \
     --runtime python3.9 \
     --role arn:aws:iam::123456789012:role/lambda-ses-role \
     --timeout 10 \
     --memory-size 128
   ```

4. **Create an API Gateway**

   - Create a new REST API
   - Create resources for each endpoint (/createPortfolio, /companyResearch, /sendEmail)
   - Set up POST methods for each resource
   - Configure integration with your Lambda function
   - Deploy the API to a stage (e.g., "prod")
   - Note the API endpoint URL

### Deploying the Streamlit Application with AWS Elastic Beanstalk

1. **Create a requirements.txt file**

   ```bash
   echo "streamlit==1.18.0" > requirements.txt
   echo "boto3==1.26.45" >> requirements.txt
   ```

2. **Create an Elastic Beanstalk configuration**

   Create a file named `.ebextensions/python.config`:

   ```yaml
   option_settings:
     aws:elasticbeanstalk:container:python:
       WSGIPath: app.py
     aws:elasticbeanstalk:application:environment:
       AWS_REGION: us-east-1
       LAMBDA_BASE_URL: https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod
       USE_SES: true
       SENDER_EMAIL: your-verified-email@example.com
   ```

3. **Create a Procfile**

   ```bash
   echo "web: streamlit run app.py --server.port 5000 --server.address 0.0.0.0" > Procfile
   ```

4. **Create an application bundle**

   ```bash
   zip -r financial-assistant.zip . -x "*.git*" "lambda/*"
   ```

5. **Create an Elastic Beanstalk application and environment**

   ```bash
   aws elasticbeanstalk create-application --application-name financial-assistant
   
   aws elasticbeanstalk create-environment \
     --application-name financial-assistant \
     --environment-name financial-assistant-prod \
     --solution-stack-name "64bit Amazon Linux 2 v3.3.8 running Python 3.8" \
     --option-settings file://.ebextensions/python.config \
     --version-label initial-version \
     --cname-prefix financial-assistant
   
   aws elasticbeanstalk create-application-version \
     --application-name financial-assistant \
     --version-label initial-version \
     --source-bundle S3Bucket="elasticbeanstalk-samples",S3Key="financial-assistant.zip"
   
   aws elasticbeanstalk update-environment \
     --application-name financial-assistant \
     --environment-name financial-assistant-prod \
     --version-label initial-version
   ```

6. **Access your deployed application**

   Once the deployment is complete, you can access your application at:
   ```
   http://financial-assistant-prod.elasticbeanstalk.com
   ```

## Deploying with Docker

You can also containerize the application with Docker for deployment in container orchestration environments like ECS, EKS, or Kubernetes.

### Prerequisites

- Docker installed
- Container registry account (e.g., Docker Hub, ECR)

### Steps

1. **Create a Dockerfile**

   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
   ```

2. **Build the Docker image**

   ```bash
   docker build -t financial-assistant:latest .
   ```

3. **Test the Docker image locally**

   ```bash
   docker run -p 5000:5000 \
     -e AWS_ACCESS_KEY_ID=your_access_key \
     -e AWS_SECRET_ACCESS_KEY=your_secret_key \
     -e AWS_REGION=us-east-1 \
     financial-assistant:latest
   ```

4. **Push the image to a container registry**

   ```bash
   # For Docker Hub
   docker tag financial-assistant:latest yourusername/financial-assistant:latest
   docker push yourusername/financial-assistant:latest
   
   # For AWS ECR
   aws ecr create-repository --repository-name financial-assistant
   aws ecr get-login-password | docker login --username AWS --password-stdin your-account-id.dkr.ecr.region.amazonaws.com
   docker tag financial-assistant:latest your-account-id.dkr.ecr.region.amazonaws.com/financial-assistant:latest
   docker push your-account-id.dkr.ecr.region.amazonaws.com/financial-assistant:latest
   ```

5. **Deploy to your container orchestration platform**

   Follow the specific deployment instructions for your container platform (ECS, EKS, Kubernetes, etc.).

## Environment Variables

These environment variables can be set to configure the application:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| AWS_ACCESS_KEY_ID | AWS access key | None |
| AWS_SECRET_ACCESS_KEY | AWS secret key | None |
| AWS_REGION | AWS region | us-east-1 |
| USE_SES | Whether to use AWS SES for email | false |
| SENDER_EMAIL | Email address to send from | financial-assistant@example.com |
| LAMBDA_BASE_URL | Base URL for Lambda API | http://localhost:8000 |
| LOG_LEVEL | Logging level | INFO |

## Troubleshooting

### Common Issues

1. **Application does not start:**
   - Check if all required packages are installed
   - Verify that the Python version is 3.9 or higher
   - Check for syntax errors in the code

2. **AWS services not working:**
   - Verify AWS credentials are set correctly
   - Check IAM permissions for the services being used
   - Ensure the region is set correctly

3. **Email functionality not working:**
   - Verify that the sender email is verified in SES
   - Check if SES is still in sandbox mode (requires recipient verification)
   - Check IAM permissions for SES

4. **Lambda function errors:**
   - Check CloudWatch logs for error details
   - Verify API Gateway configuration
   - Ensure the Lambda function has the necessary permissions

### Getting Help

If you encounter issues not covered here:
1. Check the AWS documentation for specific service issues
2. Consult the Streamlit documentation for UI-related problems
3. Open an issue in the project's GitHub repository