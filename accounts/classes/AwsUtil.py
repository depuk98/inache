import json
import boto3
import base64
import os 


class AwsUtil:
    def __init__(self, access_key_id, secret_access_key, region_name):
        self.sns_client = boto3.client(
            'sns',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )

        self.ses_client = boto3.client(
            'ses',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )


    def publish_message_to_sns(self, topic_arn, message_data):
        try:
            response = self.sns_client.publish(
                TopicArn=topic_arn,
                Message=json.dumps({'default': json.dumps(message_data)}),
                MessageStructure='json',
            )
            count=count + 1
        
            print(f'Message sent to SNS topic with message ID: {response["MessageId"]}')
            return response
        except Exception as e:
            print(f'Error publishing message to SNS: {e}')
            raise




    def send_email_via_ses(self, sender_email, recipient_emails, subject, body_html):
        try:
            # Compose the email
            message = {
                'Subject': {'Data': subject},
                'Body': {
                    'Html': {'Data': body_html},
                }
            }
            # Send the email
            response = self.ses_client.send_email(
                Source=sender_email,
                Destination={'ToAddresses': recipient_emails},
                Message=message,
            )
            count=count + 1
            # Optionally, log or handle the response from SES
            print(f'Email sent with message ID: {response["MessageId"]}')
            return response
        except Exception as e:
            # Handle exceptions as needed (logging, error reporting, etc.)
            print(f'Error sending email: {e}')
            raise

    
