import os
import logging
from flask import Flask, request, jsonify
from task import send_email  # Import Celery task
from datetime import datetime

app = Flask(__name__)

# Specific log file path for the messaging system
LOG_FILE_PATH = "/var/log/messaging.log"
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)  # Ensure log directory exists

# Set up logging with more detailed configuration
logging.basicConfig(
    filename=LOG_FILE_PATH, 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/sendmail")
def send_email_route():
    """Handles email sending requests via Celery."""
    to_email = request.args.get("sendmail")
    if not to_email:
        logging.warning(f"Sendmail request without email from {request.remote_addr}")
        return jsonify({
            "status": "error",
            "message": "No email provided. Use ?sendmail=your_email@example.com"
        }), 400

    try:
        # Queue the email task
        task = send_email.delay(to_email)
        
        logging.info(f"Email task queued for {to_email} from {request.remote_addr}")
        return jsonify({
            "status": "success",
            "message": f"Email to {to_email} is being processed",
            "task_id": str(task.id)
        }), 202
    except Exception as e:
        logging.error(f"Error queueing email task: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to queue email task"
        }), 500

@app.route("/talktome")
def talktome():
    """Logs the current time and returns a success response."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"TalkToMe request received from {request.remote_addr} at {current_time}"
    logging.info(log_message)
    return jsonify({
        "status": "success",
        "message": "Hello, I logged this!",
        "timestamp": current_time,
        "remote_addr": request.remote_addr
    }), 200

@app.route("/logs")
def get_logs():
    """Retrieves the last 100 lines of application logs."""
    try:
        with open(LOG_FILE_PATH, "r") as log_file:
            # Read last 100 lines to prevent overwhelming response
            logs = log_file.readlines()[-100:]
        return jsonify({
            "status": "success",
            "total_log_lines": len(logs),
            "logs": logs
        }), 200
    except FileNotFoundError:
        logging.error("Log file not found when accessing /logs")
        return jsonify({
            "status": "error",
            "message": "Log file not found"
        }), 404
    except Exception as e:
        logging.error(f"Error reading log file: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error reading logs: {str(e)}"
        }), 500

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "endpoints": {
            "/sendmail": "Send an email (use ?sendmail=your_email)",
            "/talktome": "Log current time",
            "/logs": "View application logs"
        }
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)