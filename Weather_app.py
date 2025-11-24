import sys
from urllib import response
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit )
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City Name:",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton( "Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
#        self.result_area = QTextEdit(self)
        self.init_ui()
#        self.get_weather_button.clicked.connect(self.fetch_weather)
        
   
    
    def init_ui(self):
        self.setWindowTitle("Weather App")
        Vbox = QVBoxLayout()
        
        Vbox.addWidget(self.city_label)
        Vbox.addWidget(self.city_input)
        Vbox.addWidget(self.get_weather_button)
        Vbox.addWidget(self.temperature_label)
        Vbox.addWidget(self.emoji_label)
        Vbox.addWidget(self.description_label)
        
        self.setLayout(Vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName("city_Label")
        self.city_input.setObjectName("city_Input")
        self.temperature_label.setObjectName("temperature_Label")
        self.emoji_label.setObjectName("emoji_Label")
        self.description_label.setObjectName("description_Label")

        self.setStyleSheet("""
            QLabel, QPushButton, QLineEdit {
               font-family: calibri;
       
            }
            QLabel#city_Label { font-size: 40px; font-style: italic; }
            QLineEdit#city_Input { font-size:  40px; }
            QPushButton#get_weather_button { font-size: 40px; padding: 10px; font-weight: bold; }
            QLabel#temperature_Label { font-size: 75px; }
            QLabel#emoji_Label { font-size: 100px; font-family: Segoe UI emoji; }
            QLabel#description_Label { font-size: 50px; font-style: italic; }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)

     
    def get_weather(self):
        
       api_key = "6c2c740fb86ca1a97420d64fae7a1e0f"
       city = self.city_input.text()
       url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

       try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
           
           
            if data["cod"] == 200:
                self.display_weather(data)
                
            
       except requests.exceptions.HTTPError as http_error:

           match http_error.response.status_code:
                case 400:
                   self.display_error(" Client Error Code 400 - Bad Request")
                case 401:
                   self.display_error(" Client Error Code 401 - Unauthorised - Invalid API Key")
                case 403:
                   self.display_error(" Client Error Code 403 - Forbidden - Access Denied")
                case 404:
                   self.display_error(" Client Error Code 404 - City Not Found")
                case 500:
                   self.display_error(" Server Error Code 500 - Internal Server Error")
                case 502:
                   self.display_error("Server Error Code 502 - Bad Gateway")
                case 503:
                   self.display_error("Server Error Code 503 - Service Unavailable")
                case 504:
                   self.display_error("Server Error Code 504 - Gateway Timeout")
                case _:
                   self.display_error(f"An error occurred while fetching data. HTTP Error \n{http_error}")

       except requests.exceptions.ConnectionError:
           self.display_error("Failed to connect to the server.")
       except requests.exceptions.Timeout:
           self.display_error("Request timed out.")
       except requests.exceptions.TooManyRedirects:
           self.display_error("Too many redirects.")
       except requests.exceptions.RequestException as req_error:
           self.display_error(f"An error occurred while fetching data. {req_error}")

    def display_error(self, message):
       self.description_label.setText(message)
       self.temperature_label.clear()
       self.emoji_label.clear()


    def display_weather(self, data):
        temp = data["main"]["temp"]
        emoji = self.get_emoji(data["weather"][0]["id"])   
        weather_description = data["weather"][0]["description"].capitalize()
        print(data)
        print(weather_description)
        
        self.temperature_label.setText(f"{temp:.0f} °C")
        self.emoji_label.setText(emoji)
        self.description_label.setText(weather_description)
        
    def get_emoji(self, weather_id):
        if 200 <= weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 400:
            return "🌦️"  # Drizzle
        elif 500 <= weather_id < 600:
            return "🌧️"  # Rain
        elif 600 <= weather_id < 700:
            return "❄️"  # Snow
        elif 700 <= weather_id < 800:
            return "🌫️"  # Atmosphere
        elif weather_id == 800:
            return "☀️"  # Clear
        elif 801 <= weather_id < 900:
            return "☁️"  # Clouds
        else:
            return "🌈"  # Default/Fallback

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
