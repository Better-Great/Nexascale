# Project Overview
This is a simple email messaging system built using:

- **Flask** (to handle HTTP requests)
- **Celery** (for background task processing)
- **RabbitMQ** (as the message broker)

The application allows users to send emails asynchronously through a queue.

## Project Structure
1. `app.py` → Handles API requests and triggers email tasks.
2. `task.py` → Processes email sending using Celery.
3. `test.py` → Used for testing email functionality.

## How to Test the Application
If the application is already running, you can test it by making a request using CURL or a browser.

### Send an Email Request
```sh 
curl "http://127.0.0.1:5000/sendmail?sendmail=abiegbegreat@gmail.com"
or 
http://127.0.0.1:5000/sendmail?sendmail=abiegbegreat@gmail.com
```
If successful, you should see:
```sh
{
  "message": "Email to abiegbegreat@gmail.com is being processed"
}
```
### Check Celery Worker Logs
If you want to see the email processing logs, run
```sh
celery -A task worker --loglevel=info
```
### Accessing the Application from Another Device
If the application is running on a remote server, replace 127.0.0.1 with your server's IP.

For example:
```sh
curl "http://YOUR_SERVER_IP:5000/sendmail?sendmail=example@gmail.com"
```
Ensure the firewall allows traffic on port 5000.

## Stopping the Application
To stop the Flask app:
```sh
Ctrl + C
```
To stop the Celery worker:
```sh
pkill -f "celery"
```

