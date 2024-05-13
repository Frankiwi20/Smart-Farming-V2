
import pandas as pd
import json

class DataGatherer:
    def __init__(self, filename="polygon_data.txt"):
        self.filename = filename

    def save_data(self, data):
        """Save the data to a file with improved formatting."""
        # Split the data into separate lines based on your GUI's display logic
        data_lines = data.split('\n')
        formatted_data = json.dumps(data_lines, indent=4)  # Use JSON to indent for readability

        with open(self.filename, 'a') as file:
            file.write(formatted_data + '\n')
            print(f"Data saved to {self.filename} in a formatted manner.")

    import pandas as pd
    import json

    def parse_data(filename):
        with open(filename, 'r') as file:
            data = file.read().splitlines()

        # Initialize variables to hold content
        poly_info = {}
        records = []

        # Extract data
        for line in data:
            if line.startswith("ID:"):
                poly_info['id'] = line.split("ID: ")[1].strip()
            elif line.startswith("Name:"):
                poly_info['name'] = line.split("Name: ")[1].strip()
            elif line.startswith("Coordinates:"):
                poly_info['coordinates'] = json.loads(line.split("Coordinates: ")[1].strip())
            elif line.startswith("Condition:"):
                poly_info['weather_condition'], temp = line.split(", Temp: ")
                poly_info['temperature'] = float(temp.replace("°C", "").strip())
            elif line.startswith("Surface Temp:"):
                temps = line.split(", ")
                poly_info['surface_temp_k'] = float(temps[0].split(" ")[2])
                poly_info['surface_temp_c'] = float(temps[1].split(" ")[0])
                poly_info['surface_temp_f'] = float(temps[2].split(" ")[0])
            elif line.startswith("Depth Temp:"):
                temps = line.split(", ")
                poly_info['depth_temp_k'] = float(temps[0].split(" ")[2])
                poly_info['depth_temp_c'] = float(temps[1].split(" ")[0])
                poly_info['depth_temp_f'] = float(temps[2].split(" ")[0])
            elif line.startswith("Moisture:"):
                poly_info['moisture'] = float(line.split("Moisture: ")[1])
                records.append(poly_info.copy())  # Save record and reset for next polygon
                poly_info = {}

        # Convert list of dicts to DataFrame
        df = pd.DataFrame(records)
        return df

    # Example use
    df = parse_data('polygon_data.txt')
    print(df.head())
