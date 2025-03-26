import os
import smtplib
from celery import Celery

# Load environment variables for email credentials
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# RabbitMQ broker URL (default port is 5672)
CELERY_BROKER_URL = "pyamqp://guest@localhost//"

# Initialize Celery
celery = Celery("tasks", broker=CELERY_BROKER_URL)

@celery.task
def send_email(to_email):
    """Send an email using SMTP via Celery."""
    try:
        with smtplib.SMTP("smtp.gmail.com", 465) as server:
            server.starttls()  # Secure connection
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

            # Email content
            subject = "Test Email from RabbitMQ & Celery"
            body = "Hello, this is a test email from your messaging system!"
            message = f"Subject: {subject}\n\n{body}"

            # Send email
            server.sendmail(EMAIL_HOST_USER, to_email, message)

        print(f"✅ Email successfully sent to {to_email}")
        return f"Email sent to {to_email}"

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return f"Error: {str(e)}"
