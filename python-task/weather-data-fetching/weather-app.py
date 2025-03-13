import os
import sys
import requests
from dotenv import load_dotenv
import json
from datetime import datetime


class WeatherApp:
    """
    A class to fetch and display weather information for cities using the OpenWeatherMap API.
    """
    
    def __init__(self):
        """Initialize the WeatherApp with API key and base URL."""
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        
        if not self.api_key:
            print("Error: API key not found. Please set the OPENWEATHER_API_KEY in your .env file.")
            sys.exit(1)
            
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def kelvin_to_celsius(self, kelvin):
        """Convert temperature from Kelvin to Celsius."""
        return round(kelvin - 273.15, 1)
    
    def fetch_weather(self, city):
        """
        Fetch weather data for a given city.
        
        Args:
            city (str): Name of the city to fetch weather for
            
        Returns:
            dict: Processed weather data or None if an error occurred
        """
        params = {
            "q": city,
            "appid": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            
            # Process the data into a more usable format
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
            if response.status_code == 404:
                print(f"City '{city}' not found. Please check the spelling.")
            else:
                print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Connection error. Please check your internet connection.")
        except requests.exceptions.Timeout:
            print("Request timed out. Please try again later.")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred: {err}")
        except KeyError:
            print("Unexpected response format from the API.")
        
        return None
    
    def display_weather(self, weather_data):
        """
        Display weather information in a formatted way.
        
        Args:
            weather_data (dict): Processed weather data
        """
        if not weather_data:
            return
            
        print(f"\nWeather in {weather_data['city']}, {weather_data['country']}:")
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Condition: {weather_data['condition']}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Wind Speed: {weather_data['wind_speed']} m/s")
        print(f"Last Updated: {weather_data['timestamp']}")
    
    def save_to_json(self, all_weather_data, filename="weather_data.json"):
        """
        Save weather data to a JSON file.
        
        Args:
            all_weather_data (list): List of weather data dictionaries
            filename (str): Name of the file to save to
        """
        with open(filename, 'w') as f:
            json.dump(all_weather_data, f, indent=4)
        print(f"\nWeather data saved to {filename}")


def main():
    """Main function to run the weather app."""
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
        
        # If we have data and more than one city, offer to save to JSON
        if all_weather_data and len(cities) > 1:
            save_option = input("\nWould you like to save this data to a JSON file? (y/n): ").lower()
            if save_option == 'y':
                weather_app.save_to_json(all_weather_data)


if __name__ == "__main__":
    main()