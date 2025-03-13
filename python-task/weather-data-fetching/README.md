# Weather App
A Python application that fetches and displays current weather information for cities around the world using the OpenWeatherMap API.
## Features

- Get real-time weather data including temperature, conditions, humidity, and wind speed
- Support for querying multiple cities at once
- Temperature conversion from Kelvin to Celsius
- Error handling for common API and network issues
- Option to save weather data to a JSON file
- Simple command-line interface

## Requirements
- Python 3.6 or higher
- `requests` library for making API calls
- `python-dotenv` library for handling environment variables

## Installation
1. Clone or download this repository to your local machine.
2. Create a virtual environment (recommended):
```sh
python -m venv weather_env
```
3. Activate the virtual environment
```sh
source venv/bin/activate
```
4. Install the required packages
```sh
pip install requests python-dotenv
```
5. Get an API key from OpenWeatherMap:

- Create a free account at [OpenWeatherMap](https://home.openweathermap.org/)
- Go to your account dashboard and find or generate an API key
- Note: New API keys may take a few hours to activate
6. Create a `.env` file in the project directory with your API key:
```sh
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage
1. Run the script:
```sh
python weather_app.py
```
2. Enter a city name when prompted (e.g., "London")
3. For multiple cities, separate them with commas (e.g., "London, Paris, Tokyo")
4. Type "exit" to quit the application
5. If you query multiple cities, you'll be asked if you want to save the data to a JSON file
