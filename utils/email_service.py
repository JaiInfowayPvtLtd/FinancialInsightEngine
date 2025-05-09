import logging
import os
import boto3
from botocore.exceptions import ClientError

class EmailService:
    """
    Service for sending emails using AWS SES or simulating email sending
    """
    
    def __init__(self, config):
        """
        Initialize the email service
        
        Args:
            config (dict): Configuration settings for the service
        """
        self.config = config
        self.use_ses = config.get('use_ses', False)
        self.sender_email = config.get('sender_email', 'financial-assistant@example.com')
        logging.info("Email Service initialized")
    
    def send_email(self, to_address, subject, body):
        """
        Send an email to the specified address
        
        Args:
            to_address (str): Recipient email address
            subject (str): Email subject line
            body (str): Email body content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not to_address:
            logging.warning("No recipient email address provided")
            return False
        
        if self.use_ses:
            return self._send_via_ses(to_address, subject, body)
        else:
            return self._simulate_email_sending(to_address, subject, body)
    
    def _send_via_ses(self, to_address, subject, body):
        """
        Send email using AWS SES
        
        Args:
            to_address (str): Recipient email address
            subject (str): Email subject line
            body (str): Email body content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Get AWS credentials from environment variables
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            aws_region = os.environ.get('AWS_REGION', 'us-east-1')
            
            # Create SES client
            ses_client = boto3.client(
                'ses',
                region_name=aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
            
            # Send email
            response = ses_client.send_email(
                Source=self.sender_email,
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
            
            logging.info(f"Email sent via SES: {response['MessageId']}")
            return True
            
        except ClientError as e:
            logging.error(f"Failed to send email via SES: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error sending email via SES: {str(e)}")
            return False
    
    def _simulate_email_sending(self, to_address, subject, body):
        """
        Simulate sending an email (for development/testing)
        
        Args:
            to_address (str): Recipient email address
            subject (str): Email subject line
            body (str): Email body content
            
        Returns:
            bool: True (simulation always succeeds)
        """
        logging.info(f"[SIMULATED EMAIL] To: {to_address}, Subject: {subject}")
        logging.info(f"[SIMULATED EMAIL] Body: {body[:100]}...")
        return True
