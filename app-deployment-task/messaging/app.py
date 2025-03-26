import os
import logging
from flask import Flask, request, jsonify
from task import send_email  # Import Celery task
from datetime import datetime
import smtplib

app = Flask(__name__)


# Log file path
LOG_FILE_PATH = "/var/log/messaging.log"

# Set up logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")

@app.route("/sendmail")
def send_email_route():
    """Handles email sending requests via Celery."""
    to_email = request.args.get("sendmail")
    if not to_email:
        return jsonify({"error": "No email provided"}), 400

    send_email.delay(to_email)  # Queue the email task
    return jsonify({"message": f"Email to {to_email} is being processed"}), 202

@app.route("/talktome")
def log_time():
    """Logs the current time and returns a success response."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"User accessed /talktome at {current_time}"
    
    # Write to log file
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_message + "\n")

    return jsonify({"message": "Logged successfully"}), 200

@app.route("/logs")
def get_logs():
    """Retrieves the application logs."""
    try:
        with open(LOG_FILE_PATH, "r") as log_file:
            logs = log_file.readlines()
        return jsonify({"logs": logs}), 200
    except FileNotFoundError:
        return jsonify({"error": "Log file not found"}), 404

@app.route("/")
def home():
    return "Messaging System is Running!", 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
