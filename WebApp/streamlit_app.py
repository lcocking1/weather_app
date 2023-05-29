import streamlit as st
import folium
from streamlit_folium import st_folium
from azure.cosmos import CosmosClient
import json 
import sys
from get_grid_id import get_grid_id
import pandas as pd

sys.path.append("../FunctionApp")

from get_weather_data import GetWeatherData

gwd = GetWeatherData()

cred = json.load(open("access_control.json"))

# @st.cache_data
# def get_clients():
cosmos_client = CosmosClient(
    url=cred["gencosmos"]["URI"],
    credential=cred["gencosmos"]["PRIMARY KEY"]
)

db_client = cosmos_client.get_database_client("cosmos_dev")

forecast_client = db_client.get_container_client("forecast_hourly")
gridpoints_client = db_client.get_container_client("gridpoints")
    # return (forecast_client, gridpoints_client)

# (forecast_client, gridpoints_client) = get_clients()

grid_items = gridpoints_client.read_all_items()

grid_items_list = list(grid_items)

df_grid_items = pd.DataFrame(grid_items_list)
df_grid_items["coordinates"] = df_grid_items["coordinates"].apply(lambda x: gwd.search_coordinates(x))

coordinates = []

# for i in range(len(grid_items_list)):
#     # coordinates += gwd.search_coordinates(i["coordinates"])
#     grid_items_list[i]['coordinates'] = gwd.search_coordinates(grid_items_list[i]['coordinates'])

# coordinates += [i['coordinates'] for i in grid_items_list]
# for i in grid_items_list:
#     coordinates += i['coordinates']
for i in df_grid_items["coordinates"].to_list():
    coordinates += i

# fix longitude/latitude
# print(coordinates)
# print('\n\n')
coordinates = [[c[1], c[0]] for c in coordinates]
# print(coordinates)

m = folium.Map(location=coordinates[0])

fg = folium.FeatureGroup(name="Forecast Locations")

for c in coordinates:
    folium.Marker(c).add_to(m)

col1, col2 = st.columns(2)

col1 = st_folium(m, width=725)

clicked_location = col1["last_clicked"]

if clicked_location is not None:
    df_grid_id = get_grid_id(clicked_location, df_grid_items)
    # st.write(grid_id)

    # in a separate visual, display the forecast info for that grid
    sql_select = "select c.properties.periods from c"
    sql_where = f"where c.gridId = '{df_grid_id['gridId']}' and c.gridX = '{df_grid_id['gridX']}' and c.gridY = '{df_grid_id['gridY']}'"
    sql = f"{sql_select} {sql_where}"

    forecast_item = [i["periods"] for i in forecast_client.query_items(sql, enable_cross_partition_query=True)]
    df = pd.DataFrame(forecast_item[0])
    for item in forecast_item[1:]:
        df = pd.concat([df, pd.DataFrame(item)], ignore_index=True)
    col2 = st.dataframe(df)