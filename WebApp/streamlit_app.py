import streamlit as st
import folium
from streamlit_folium import st_folium
from azure.cosmos import CosmosClient
import json 

cred = json.load(open("access_control.json"))

cosmos_client = CosmosClient(
    url=cred["gencosmos"]["URI"],
    credential=cred["gencosmos"]["PRIMARY KEY"]
)

db_client = cosmos_client.get_database_client("cosmos_dev")

forecast_client = db_client.get_container_client("forecast_hourly")
gridpoints_client = db_client.get_container_client("gridpoints")

grid_items = gridpoints_client.read

# forecast_items = list(c.forecast_client.read_all_items())
# coordinates_list = c.clean_coordinate_list(coordinates_raw)

# m = folium.Map(location=coordinates_list[0])

# fg = folium.FeatureGroup(name="Forecast Locations")

# for c in coordinates_list:
#     folium.Marker(c).add_to(m)


# st_data = st_folium(m, width=725)

m = folium.Map(location=[0,0])

m.add_child(folium.ClickForMarker())

st_data = st_folium(m, width=725)

clicked_location = st_data['last_clicked']

if clicked_location is not None:
    st.write(clicked_location)