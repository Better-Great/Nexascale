import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery
import logging

# Load environment variables for email credentials
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    raise ValueError("EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set in environment")

# RabbitMQ broker URL (default port is 5672)
CELERY_BROKER_URL = "pyamqp://guest@localhost//"

# Initialize Celery
celery = Celery("tasks", broker=CELERY_BROKER_URL)

# Configure logging
logging.basicConfig(
    filename="/var/log/messaging.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@celery.task(bind=True, max_retries=3)
def send_email(self, to_email):
    """Send an email using SMTP via Celery with enhanced error handling."""
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = to_email
        msg['Subject'] = "Test Email from Messaging System"

        # Email body
        body = f"Hello!\n\nThis is a test email sent to {to_email} via our messaging system.\n\nRegards,\nMessaging System"
        msg.attach(MIMEText(body, 'plain'))

        # Establish secure connection
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.ehlo()
            print("EHLO successful")
            print(f"Attempting login with {EMAIL_HOST_USER}")
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            print("Login successful")
            server.send_message(msg)
            print("Message sent successfully")

        logging.info(f"✅ Email successfully sent to {to_email}")
        return f"Email sent to {to_email}"

    except Exception as exc:
        logging.error(f"❌ Failed to send email to {to_email}: {str(exc)}")
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)