import requests
import json

class GetWeatherData:
    def __init__(self) -> None:
        self.weather_session = requests.Session()
        self.external_host = "https://api.weather.gov"

    def download_file(self, url_branch, params={}, type='GET'):
        url = f"{self.external_host}/{url_branch}"
        # print(url, params)
        response = self.weather_session.request(method=type, url=url, params=params)
        if response.status_code == 200:
            return response.json()
        return {"error": response.text}
    
    def get_county_metadata(self):
        ''' get county metadata {id, name, eff/expir date, state, cwa(nws office)} '''
        counties = self.download_file('zones', params={"type": "county"})
        counties_clean = []
        for county in counties["features"]:
            temp_d = {}
            temp_d["id"] = county["properties"]["id"]
            temp_d["name"] =county["properties"]["name"]
            temp_d["effectiveDate"] = county["properties"]["effectiveDate"]
            temp_d["expirationDate"] = county["properties"]["expirationDate"]
            temp_d["state"] = county["properties"]["state"]
            temp_d["cwa"] = county["properties"]["cwa"]
            counties_clean.append(temp_d)
        return counties_clean

    def get_county_details(self, county_id):
        ''' return county details for county_id '''
        detail_data = self.download_file(f'zones/county/{county_id}')
        coordinate_list = detail_data["geometry"]["coordinates"]
        coordinates = self.search_coordinates(coordinate_list)
        return {"coordinates": coordinates}

    def get_gridpoints(self, coordinates):
        '''for coordinate in coordinates, return points json'''
        points_data = []
        for coordinate in coordinates:
            path = f'points/{coordinate[1]},{coordinate[0]}'
            points_data.append(self.download_file(path))
        return points_data

    def search_coordinates(self, coordinate_list):
        ''' parse through coordinates list to get desired output '''
        if coordinate_list != [] and type(coordinate_list[0][0]) != float:
            return self.search_coordinates(coordinate_list[0]) + self.search_coordinates(coordinate_list[1:])
        return coordinate_list