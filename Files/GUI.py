import json
import random
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QDialog, QFormLayout
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPalette, QBrush, QImage
from data import DataGatherer
from graphs import GraphCreator  # Import GraphCreator class from graphs.py
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

class GUI(QWidget):
    def __init__(self, api_manager):
        super().__init__()
        self.api_manager = api_manager
        self.data_gatherer = DataGatherer()  # Instance of DataGatherer
        self.graph_creator = GraphCreator()  # Instance of GraphCreator
        self.polygon_ids = []  # Store entered polygon IDs
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('Smart Farming Application')
        self.setFixedSize(1200, 800)
        self.setupBackground()
        self.setupLoginScreen()
        self.setupMainUI()

    def setupBackground(self):
        try:
            oImage = QImage("C:\\Users\\hashe\\Downloads\\FarmLandscapeBackground.jpg")
            sImage = oImage.scaled(QSize(1200, 800))  # Resize image to widget size
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sImage))
            self.setPalette(palette)
        except Exception as e:
            print(f"Error setting background: {e}")

    def setupLoginScreen(self):
        try:
            self.login_dialog = QDialog(self)
            self.login_dialog.setWindowTitle('Login')
            self.login_dialog.setStyleSheet("font-size: 12pt; font-weight: bold; color: white; background-color: rgba(144, 238, 144, 0.8); padding: 20px;")
            login_layout = QFormLayout()
            self.username_input = QLineEdit()
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            login_button = QPushButton("Login")
            login_button.clicked.connect(self.checkLogin)
            login_layout.addRow("Username:", self.username_input)
            login_layout.addRow("Password:", self.password_input)
            login_layout.addRow(login_button)
            self.login_dialog.setLayout(login_layout)
            self.login_dialog.exec_()
        except Exception as e:
            print(f"Error setting up login screen: {e}")

    def checkLogin(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "Farmer John" and password == "Farms":
            self.login_dialog.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password. Go away!")
            self.login_dialog.reject()
            self.close()

    def setupMainUI(self):
        try:
            self.layout = QVBoxLayout()
            welcome_label = QLabel('AgriLock')
            welcome_label.setAlignment(Qt.AlignCenter)
            welcome_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: white; background-color: rgba(0, 100, 0, 150); padding: 10px;")
            self.layout.addWidget(welcome_label)

            self.polygon_input = QLineEdit()
            self.polygon_input.setPlaceholderText("Enter Polygon ID")
            self.polygon_input.setStyleSheet("background-color: rgba(255, 255, 255, 100); font-size: 18pt; padding: 5px;")
            self.layout.addWidget(self.polygon_input)

            fetch_button = QPushButton('Fetch Data')
            fetch_button.setStyleSheet("QPushButton { background-color: rgba(0, 100, 0, 100); color: white; font-weight: bold; padding: 10px; border: none; } QPushButton:hover { background-color: rgba(0, 150, 0, 100); }")
            fetch_button.clicked.connect(self.onFetchData)
            self.layout.addWidget(fetch_button)

            self.polygon_name_input = QLineEdit()
            self.polygon_name_input.setPlaceholderText("Enter Polygon Name")
            self.polygon_name_input.setStyleSheet("background-color: rgba(255, 255, 255, 100); font-size: 18pt; padding: 5px;")
            self.layout.addWidget(self.polygon_name_input)

            fetch_name_button = QPushButton('Get Poly Name Data')
            fetch_name_button.setStyleSheet("QPushButton { background-color: rgba(0, 0, 100, 100); color: white; font-weight: bold; padding: 10px; border: none; } QPushButton:hover { background-color: rgba(0, 0, 150, 100); }")
            fetch_name_button.clicked.connect(self.onFetchDataByName)
            self.layout.addWidget(fetch_name_button)

            self.satellite_button = QPushButton('Fetch Satellite Imagery')
            self.satellite_button.setStyleSheet("QPushButton { background-color: rgba(0, 0, 100, 100); color: white; font-weight: bold; padding: 10px; border: none; } QPushButton:hover { background-color: rgba(0, 0, 150, 100); }")
            self.satellite_button.clicked.connect(self.onFetchSatelliteImagery)
            self.layout.addWidget(self.satellite_button)

            self.data_display = QTextEdit()
            self.data_display.setReadOnly(True)
            self.data_display.setStyleSheet("background-color: rgba(255, 255, 255, 100); font-size: 16pt;")
            self.layout.addWidget(self.data_display)

            save_data_button = QPushButton('Save Data')
            save_data_button.clicked.connect(self.saveDisplayedData)
            self.layout.addWidget(save_data_button)

            corrupt_data_button = QPushButton('Corrupt Data')
            corrupt_data_button.clicked.connect(self.corruptDisplayedData)
            self.layout.addWidget(corrupt_data_button)

            graph_data_button = QPushButton('Graph Data')
            graph_data_button.setStyleSheet("QPushButton { background-color: rgba(100, 0, 0, 100); color: white; font-weight: bold; padding: 10px; border: none; } QPushButton:hover { background-color: rgba(150, 0, 0, 100); }")
            graph_data_button.clicked.connect(self.graphData)
            self.layout.addWidget(graph_data_button)

            self.setLayout(self.layout)
        except Exception as e:
            print(f"Error setting up main UI: {e}")

    def graphData(self):
        try:
            # Call create_bar_chart method from the GraphCreator instance
            self.graph_creator.create_bar_chart('polygon_data.txt')
        except Exception as e:
            print(f"Error creating graph: {e}")

    # Other methods remain the same...

    def onFetchData(self):
        polygon_id = self.polygon_input.text().strip()
        if polygon_id:
            self.polygon_ids.append(polygon_id)
            try:
                polygon_data = self.api_manager.get_polygon_data(polygon_id)
                self.display_polygon_data(polygon_data)
                self.fetch_weather_data(polygon_data)
                self.fetch_soil_data(polygon_id)
                self.askForAnotherPolygon()
            except Exception as e:
                self.data_display.setText(f"Error retrieving data: {str(e)}")

    def onFetchDataByName(self):
        polygon_name = self.polygon_name_input.text().strip()
        if polygon_name:
            try:
                polygon_data = self.api_manager.get_polygon_data_by_name(polygon_name)
                self.display_polygon_data(polygon_data)
                self.fetch_weather_data(polygon_data)
                self.fetch_soil_data(polygon_data['id'])
            except Exception as e:
                self.data_display.setText(f"Error retrieving data: {str(e)}")

    def askForAnotherPolygon(self):
        reply = QMessageBox.question(self, 'Fetch More Data', "Do you want to enter another Polygon ID?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.polygon_input.clear()
            self.polygon_input.setFocus()

    def display_polygon_data(self, polygon_data):
        self.data_display.append("Polygon Data:")
        self.data_display.append(f"ID: {polygon_data.get('id', 'N/A')}")
        self.data_display.append(f"Name: {polygon_data.get('name', 'N/A')}")
        coordinates = polygon_data.get('geo_json', {}).get('geometry', {}).get('coordinates', [])
        self.data_display.append(f"Coordinates: {json.dumps(coordinates)}")
        self.data_display.append("")

    def onFetchSatelliteImagery(self):
        polygon_id = self.polygon_input.text().strip()
        if polygon_id:
            try:
                imagery_links = self.api_manager.get_satellite_imagery(polygon_id)
                self.display_satellite_imagery_links(imagery_links)
            except Exception as e:
                QMessageBox.critical(self, "Satellite Imagery Error", str(e))

    def display_satellite_imagery_links(self, imagery_links):
        self.data_display.append("Satellite Imagery Links:")
        for link_type, url in imagery_links.items():
            self.data_display.append(f"{link_type}: {url}")
            self.data_display.append("")
        self.data_display.append("Click the links to open satellite images.")

    def fetch_weather_data(self, polygon_data):
        coordinates = polygon_data.get('geo_json', {}).get('geometry', {}).get('coordinates', [])
        lat, lon = self.api_manager.calculate_centroid(coordinates)
        weather_data = self.api_manager.get_weather_by_coordinates(lat, lon)
        self.display_weather_data(weather_data)

    def display_weather_data(self, weather_data):
        self.data_display.append("Weather Data:")
        weather_description = weather_data['weather'][0]['description']
        temp_celsius = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
        self.data_display.append(f"Condition: {weather_description}, Temp: {temp_celsius:.2f}°C")
        self.data_display.append("")  # Add a newline for better readability

    def fetch_soil_data(self, polygon_id):
        soil_data = self.api_manager.get_soil_data(polygon_id)
        self.display_soil_data(soil_data)

    def display_soil_data(self, soil_data):
        self.data_display.append("Soil Data:")
        surface_temp_kelvin = soil_data.get('t0', 'N/A')
        depth_temp_kelvin = soil_data.get('t10', 'N/A')
        if surface_temp_kelvin != 'N/A' and depth_temp_kelvin != 'N/A':
            surface_temp_celsius = surface_temp_kelvin - 273.15
            depth_temp_celsius = depth_temp_kelvin - 273.15
            surface_temp_fahrenheit = (surface_temp_celsius * 9/5) + 32
            depth_temp_fahrenheit = (depth_temp_celsius * 9/5) + 32
            self.data_display.append(f"Surface Temp: {surface_temp_kelvin:.2f} K, {surface_temp_celsius:.2f} °C, {surface_temp_fahrenheit:.2f} °F")
            self.data_display.append(f"Depth Temp: {depth_temp_kelvin:.2f} K, {depth_temp_celsius:.2f} °C, {depth_temp_fahrenheit:.2f} °F")
        else:
            self.data_display.append(f"Surface Temp: {surface_temp_kelvin} K")
            self.data_display.append(f"Depth Temp: {depth_temp_kelvin} K")
        self.data_display.append(f"Moisture: {soil_data.get('moisture', 'N/A')}")
        self.data_display.append("")  # Add a newline for better readability

    def fetch_accumulated_temperature_data(self, polygon_data):
        coordinates = polygon_data.get('geo_json', {}).get('geometry', {}).get('coordinates', [])
        lat, lon = self.api_manager.calculate_centroid(coordinates)
        start_date = int((datetime.utcnow() - timedelta(days=30)).timestamp())
        end_date = int(datetime.utcnow().timestamp())
        threshold = 273.15  # Example threshold in Kelvin
        try:
            accumulated_temp_data = self.api_manager.get_accumulated_temperature(lat, lon, start_date, end_date, threshold)
            self.display_accumulated_temperature_data(accumulated_temp_data)
        except Exception as e:
            self.data_display.append(f"Error retrieving accumulated temperature data: {str(e)}")

    def saveDisplayedData(self):
        try:
            data = self.data_display.toPlainText()
            with open("polygon_data.txt", "w") as file:
                file.write(data)
            QMessageBox.information(self, "Data Saved", "Data saved to polygon_data.txt successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error saving data: {str(e)}")

    def corruptDisplayedData(self):
        try:
            data = self.data_display.toPlainText().split('\n')
            random.shuffle(data)
            corrupted_data = '\n'.join(data)
            self.data_gatherer.save_corrupted_data(corrupted_data)
            self.data_display.setText(corrupted_data)
        except Exception as e:
            QMessageBox.critical(self, "Corruption Error", f"Error corrupting data: {str(e)}")
