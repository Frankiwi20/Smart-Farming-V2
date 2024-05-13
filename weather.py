import requests

class WeatherData:
    def __init__(self, api_key):
        self.api_key = api_key
        self.current_weather_url = "https://api.agromonitoring.com/agro/1.0/weather"
        self.forecast_weather_url = "https://api.agromonitoring.com/agro/1.0/weather/forecast"

    def get_weather_by_coordinates(self, lat, lon):
        return self.fetch_weather_data(lat, lon, self.current_weather_url)

    def get_weather_forecast_by_coordinates(self, lat, lon):
        return self.fetch_weather_data(lat, lon, self.forecast_weather_url)

    def fetch_weather_data(self, lat, lon, url):
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for HTTP error responses

            data = response.json()
            if url.endswith("forecast"):
                return self.format_forecast_data(data)
            return self.format_current_weather_data(data)

        except requests.RequestException as e:
            return f"Failed to retrieve weather data: {e}"  # HTTP or network error

        except (KeyError, IndexError) as e:
            return f"Error parsing weather data: {e}"  # Error in accessing data fields

        except Exception as e:
            return f"An unexpected error occurred: {e}"  # Other errors

    def format_current_weather_data(self, data):
        weather_description = data['weather'][0]['description']
        temperature_k = data['main']['temp']
        temperature_c = temperature_k - 273.15  # Convert Kelvin to Celsius
        temperature_f = (temperature_c * 9/5) + 32  # Convert Celsius to Fahrenheit
        return f"Weather: {weather_description}, Temp: {temperature_c:.2f} °C ({temperature_f:.2f} °F), Humidity: {data['main']['humidity']}%, Wind: {data['wind']['speed']} m/s"

    def format_forecast_data(self, data):
        forecasts = []
        for item in data:
            date = item['dt']
            weather_description = item['weather'][0]['description']
            temperature_k = item['main']['temp']
            temperature_c = temperature_k - 273.15  # Convert Kelvin to Celsius
            forecasts.append(f"Date: {date}, Weather: {weather_description}, Temp: {temperature_c:.2f} °C")
        return "\n".join(forecasts)

# Example usage:
weather_instance = WeatherData('caf6429d5d94023d5089fb656817efad')
lat, lon = 35, 139  # Example coordinates
weather_info = weather_instance.get_weather_by_coordinates(lat, lon)
print(weather_info)
forecast_info = weather_instance.get_weather_forecast_by_coordinates(lat, lon)
print(forecast_info)
