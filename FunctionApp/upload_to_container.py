import json
from azure.cosmos import CosmosClient, PartitionKey
from get_weather_data import GetWeatherData
import datetime as dt

class UploadToContainer:
    def __init__(self) -> None:
        c = open("access_control.json")
        cred = json.load(c)
        self.client = CosmosClient(
            url=cred["gencosmos"]["URI"],
            credential=cred["gencosmos"]["PRIMARY KEY"]
        )
        self.database_name = "cosmos_dev"
        # self.container_name = container_name
        self.db_client = self.client.get_database_client(database=self.database_name)
        # weather data init #
        self.weather_client = GetWeatherData()
        return None

    def load_items_to_container(self, items, id, partition_key):
        container_client = self.db_client.create_container_if_not_exists(
            id=id,
            partition_key=PartitionKey(partition_key)
        )
        container_client.upsert_item(items)
    
    def load_forecasts(self):
        error_list = []
        ''' load hourly forecasts for gridpoints in "gridpoints" container '''
        gridpoints_client = self.db_client.get_container_client("gridpoints")
        # get gridpoints ref data to call hourly forecast
        gridpoints = [gp for gp in gridpoints_client.read_all_items()]
        # gridpoints items are structured as: keys = [id, gridId, gridX, gridY]

        # get hourly forecast for each gridpoint, then load to forecast_hourly container
        fh_client = self.db_client.get_container_client("forecast_hourly")
        for gridpoint in gridpoints:
            url_branch = f'gridpoints/{gridpoint["gridId"]}/{gridpoint["gridX"]},{gridpoint["gridY"]}/forecast/hourly'
            fh_item = self.weather_client.download_file(url_branch=url_branch)
            if "error" not in fh_item:
                # create id for fh_item
                timestamp_string = str(
                    int(
                        dt.datetime.strptime(
                            fh_item["properties"]["generatedAt"][:-6], '%Y-%m-%dT%H:%M:%S'
                        ).timestamp()
                    )
                )
                # fh_item_id = '_'.join([gridpoint["id"], timestamp_string])
                fh_item_id = gridpoint["id"]
                # remove unneeded keys/values from fh_item
                temp_d = {}
                temp_d["id"] = fh_item_id
                # temp_d["gridpointId"] = gridpoint["id"]
                temp_d["coordinates"] = fh_item["geometry"]["coordinates"]
                temp_d["properties"] = fh_item["properties"]
                # add gridpoint info for lookup to gridpoints
                temp_d["gridId"] = gridpoint["gridId"]
                temp_d["gridX"] = gridpoint["gridX"]
                temp_d["gridY"] = gridpoint["gridY"]
                temp_d["forecast_generated_timestamp"] = timestamp_string

                fh_client.upsert_item(temp_d)
            else:
                error_list.append(fh_item)
        return error_list