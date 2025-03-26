import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load email credentials from environment variables
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")  # Load recipient email

# Ensure required environment variables are set
if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD or not EMAIL_RECIPIENT:
    raise ValueError("❌ EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, or EMAIL_RECIPIENT is not set!")

# Email details
sender_email = EMAIL_HOST_USER
recipient_email = EMAIL_RECIPIENT  # Use env variable for recipient
subject = "Test Email from Flask App"
body = "This is a test email to verify SMTP settings."

# Create email message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = recipient_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    # Connect to Gmail SMTP server (using port 465 for SSL)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print(f"✅ Test email sent successfully to {recipient_email}!")

except Exception as e:
    print(f"❌ Failed to send test email: {e}")
