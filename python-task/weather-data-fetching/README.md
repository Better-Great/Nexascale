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
It is important to note that before running the script it is important to run the `source .env` command whcih will ensure that configuration in the environment variables are easily recognized by the script. 
```sh
python weather-app.py
```
2. Enter a city name when prompted (e.g., "London")
3. For multiple cities, separate them with commas (e.g., "London, Paris, Tokyo")
4. Type "exit" to quit the application
5. If you query multiple cities, you'll be asked if you want to save the data to a JSON file

## Code Explanation
### Class Structure
The application uses a WeatherApp class to encapsulate functionality. Here's a breakdown of the code:

#### 1. Imports and Dependencies
```sh
import os
import sys
import requests
from dotenv import load_dotenv
import json
from datetime import datetime
```
- `os` and `sys`: For environment variables and system operations
- `requests`: For making HTTP API calls
- `dotenv`: For loading the API key from the environment
- `json`: For saving data to JSON files
- `datetime`: For formatting timestamps

#### 2. WeatherApp Class Initialization
```sh
def __init__(self):
    load_dotenv()
    self.api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not self.api_key:
        print("Error: API key not found. Please set the OPENWEATHER_API_KEY in your .env file.")
        sys.exit(1)
        
    self.base_url = "https://api.openweathermap.org/data/2.5/weather"
```
This part of the code:
- Loads environment variables from the `.env` file
- Gets the API key and verifies it exists
- Sets up the base URL for the API requests

#### 3. Temperature Conversion
```sh
def kelvin_to_celsius(self, kelvin):
    return round(kelvin - 273.15, 1)
```
OpenWeatherMap returns temperatures in Kelvin, so this method converts them to Celsius and rounds to one decimal place.

#### 4. Weather Data Fetching
```sh
def fetch_weather(self, city):
    params = {
        "q": city,
        "appid": self.api_key
    }
    
    try:
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        weather_info = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": self.kelvin_to_celsius(data["main"]["temp"]),
            "condition": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return weather_info
        
    except requests.exceptions.HTTPError as http_err:
        # Error handling code...
    except requests.exceptions.ConnectionError:
        # More error handling...
    
    return None
```
This method:

- Creates the parameters for the API request
- Makes the request using the requests library
- Processes the JSON response into a more usable format
- Handles various error conditions with specific messages
- Returns either the processed weather data or None if there was an error

#### 5. Weather Display
```sh
def display_weather(self, weather_data):
    if not weather_data:
        return
        
    print(f"\nWeather in {weather_data['city']}, {weather_data['country']}:")
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Condition: {weather_data['condition']}")
    print(f"Humidity: {weather_data['humidity']}%")
    print(f"Wind Speed: {weather_data['wind_speed']} m/s")
    print(f"Last Updated: {weather_data['timestamp']}")
```
This method formats and displays the weather information in a user-friendly way.

#### 6. JSON Data Saving
```sh
def save_to_json(self, all_weather_data, filename="weather_data.json"):
    with open(filename, 'w') as f:
        json.dump(all_weather_data, f, indent=4)
    print(f"\nWeather data saved to {filename}")
```
This method saves the weather data to a JSON file with proper formatting.

#### 7. Main Function
```sh
def main():
    weather_app = WeatherApp()
    
    print("Welcome to the Weather App!")
    print("Enter city names (separate multiple cities with commas, or type 'exit' to quit):")
    
    while True:
        user_input = input("\nEnter city name(s): ").strip()
        
        if user_input.lower() == 'exit':
            print("Exiting the Weather App. Goodbye!")
            break
            
        cities = [city.strip() for city in user_input.split(',')]
        all_weather_data = []
        
        for city in cities:
            weather_data = weather_app.fetch_weather(city)
            if weather_data:
                weather_app.display_weather(weather_data)
                all_weather_data.append(weather_data)
        
        if all_weather_data and len(cities) > 1:
            save_option = input("\nWould you like to save this data to a JSON file? (y/n): ").lower()
            if save_option == 'y':
                weather_app.save_to_json(all_weather_data)
```
The main function:

- Creates an instance of the WeatherApp class
- Shows welcome messages and instructions
- Enters a loop to continuously accept user input
- Processes comma-separated city names into a list
- Fetches and displays weather for each city
- Offers the option to save data to a JSON file if multiple cities were queried

#### 8. Script Entry Point
```sh
if __name__ == "__main__":
    main()
```

## Error Handling
The application implements robust error handling for different scenarios:

- HTTP errors (like 404 when a city isn't found)
- Connection errors when there's no internet
- Timeout errors when the API takes too long to respond
- General request exceptions for other issues
- KeyError handling for unexpected API response formats

## Request Flow

1. User enters city name(s)
2. For each city, an API request is made
3. The response is processed into a simplified dictionary
4. The weather information is displayed to the user
5. If multiple cities were queried, the user is offered to save the data

## Example Output
```sh
Weather in London, GB:
Temperature: 12.5°C
Condition: few clouds
Humidity: 76%
Wind Speed: 4.2 m/s
Last Updated: 2025-03-13 14:30:21
```

## Limitations
- Free tier API usage limits (60 calls per minute, 1,000,000 calls per month)
- Limited historical data access
- Some weather details only available with paid API subscriptions

## Troubleshooting
Some of the issues I enocuntered while carrying out this task was the **401 Unauthorized error:**

To resolve it, you can do the following below
- Check that your API key is correctly copied in the .env file
- Verify your API key is active (can take up to 24 hours after registration though it worked 30 mins after mine)
- Test your API key directly in a browser:
```sh
https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY
```
For other issues, check that:

- The `.env` file is in the same directory as the script
- You have an active internet connection
- City names are spelled correctly