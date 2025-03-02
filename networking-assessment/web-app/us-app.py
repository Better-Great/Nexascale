from flask import Flask, render_template_string
from datetime import datetime
import pytz

app = Flask(__name__)

# Set timezone for New York (Eastern Time)
nyc_tz = pytz.timezone("America/New_York")

# HTML Template with Different Styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>New York Time Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            text-align: center;
            background-color: #1e1e1e;
            color: #f0f0f0;
        }
        .container {
            background-color: #2a2a2a;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        .time {
            color: #00aaff;
            font-size: 1.5em;
            margin-top: 20px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>New York Time (EST/EDT)</h1>
        <p>This page shows the current date & time in New York.</p>
        <p class="time">Current Date & Time in NYC: <strong>{{ current_time }}</strong></p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    nyc_time = datetime.now(nyc_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
    return render_template_string(HTML_TEMPLATE, current_time=nyc_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
