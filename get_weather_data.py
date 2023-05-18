import requests
import json

class GetWeatherData:
    def __init__(self) -> None:
        self.weather_session = requests.Session()
        external_host = "https://api.weather.gov"