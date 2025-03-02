from flask import Flask, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# Set timezone for Lagos (West Africa Time - WAT)
lagos_tz = pytz.timezone("Africa/Lagos")

# HTML template with styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Web Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            text-align: center;
            background-color: #f0f0f0;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        .time {
            color: #666;
            font-size: 1.2em;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Simple Web Page</h1>
        <p>This is a basic Flask application running on port 8080.</p>
        <p class="time">Current Date & Time in Lagos (WAT): <strong>{{ current_time }}</strong></p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    lagos_time = datetime.now(lagos_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
    return render_template_string(HTML_TEMPLATE, current_time=lagos_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
