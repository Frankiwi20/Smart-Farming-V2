import requests
import datetime
import json

class APIManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.agromonitoring.com/agro/1.0'
        self.polygon_ids = []  # List to store polygon IDs

    def create_polygon(self, coordinates, name="Default Polygon", duplicated=False):
        """Create a polygon and store its ID."""
        url = f"{self.base_url}/polygons?appid={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        geo_json = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Polygon", "coordinates": [coordinates]}
        }
        payload = {"name": name, "geo_json": geo_json, "duplicated": duplicated}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            data = response.json()
            self.polygon_ids.append(data['id'])  # Store the new polygon ID
            return data
        else:
            response.raise_for_status()

    def get_polygon_data(self, polygon_id):
        """Retrieve data for a specific polygon ID."""
        url = f"{self.base_url}/polygons/{polygon_id}?appid={self.api_key}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else response.raise_for_status()

    def get_all_polygons(self):
        """Retrieve data for all polygons."""
        url = f"{self.base_url}/polygons?appid={self.api_key}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else response.raise_for_status()

    def get_polygon_data_by_name(self, polygon_name):
        """Retrieve data for a polygon by name."""
        polygons = self.get_all_polygons()
        for polygon in polygons:
            if polygon['name'] == polygon_name:
                return polygon
        raise Exception("Polygon with the specified name not found.")


    def calculate_centroid(self, coordinates):
        """Calculate the centroid of a set of coordinates."""
        x = [coord[0] for coord in coordinates[0]]  # Assumes that 'coordinates' is a list of lists of tuples
        y = [coord[1] for coord in coordinates[0]]
        centroid_x = sum(x) / len(x)
        centroid_y = sum(y) / len(y)
        return centroid_y, centroid_x  # Correct order for latitude, longitude

    def get_weather_by_coordinates(self, lat, lon):
        """Fetch weather data by latitude and longitude."""
        url = f"{self.base_url}/weather"
        params = {'lat': lat, 'lon': lon, 'appid': self.api_key}
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else response.raise_for_status()

    def get_satellite_imagery(self, polygon_id):
        """Retrieve satellite imagery for a polygon."""
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=30)
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        url = f"{self.base_url}/image/search?start={start_timestamp}&end={end_timestamp}&polyid={polygon_id}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch satellite imagery metadata: {response.text}")
        return response.json()

    def get_soil_data(self, polygon_id):
        """Fetch soil data for a given polygon."""
        url = f"{self.base_url}/soil?polyid={polygon_id}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to retrieve soil data: {response.text}")

if __name__ == "__main__":
    api_manager = APIManager('your_api_key_here')  # Replace 'your_api_key_here' with your actual API key
    try:
        polygon_id = 'example_polygon_id'  # Replace with a valid polygon ID
        polygon_data = api_manager.get_polygon_data(polygon_id)
        print("Polygon Data:", json.dumps(polygon_data, indent=4))
        weather_data = api_manager.get_weather_by_coordinates(37.773972, -122.431297)  # Example coordinates for San Francisco
        print("Weather Data:", json.dumps(weather_data, indent=4))
        imagery_data = api_manager.get_satellite_imagery(polygon_id)
        print("Imagery Data:", json.dumps(imagery_data, indent=4))
        soil_data = api_manager.get_soil_data(polygon_id)
        print("Soil Data:", json.dumps(soil_data, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")
