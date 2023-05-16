import requests
import json

class GetCoordinates:
    def __init__(self) -> None:
        c = open('credentials.json')
        self.cred = json.load(c)
        self.sesh = requests.Session()

    def get_coordinates(self, state: str, zipcode: str) -> list:
        location_url = "http://dev.virtualearth.net/REST/v1/Locations/US"
        test_loc = f"{state}/{zipcode}"
        response = self.sesh.get(url=f"{location_url}/{test_loc}", params={"key": self.cred["bingMapsKey"]})
        if response.status_code == 200:
            return self.parse_dict(response.json())
    
    def parse_dict(self, d: dict) -> list:
        resource_sets = d['resourceSets']
        coordinates = []
        for resource_set in resource_sets:
            if 'resources' in resource_set:
                point_sets = resource_set['resources']
                for point_set in point_sets:
                    if 'point' in point_set.keys():
                        coordinates.append(point_set['point']['coordinates'])
        return coordinates[0]
