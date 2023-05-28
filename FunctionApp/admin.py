from azure.cosmos import CosmosClient, PartitionKey
import json
cred = json.load(open("access_control.json"))

client = CosmosClient(
    url= cred["gencosmos"]["URI"],
    credential=cred["gencosmos"]["PRIMARY KEY"]
)

db_client = client.get_database_client(
    database="cosmos_dev"
)
# gridpoints_container_client = db_client.get_container_client(
#     container="gridpoints"
# )
# forecast_container_client = db_client.get_container_client("forecast_hourly")

# db_client.delete_container("forecast_hourly")

db_client.create_container(
    "forecast_hourly",
    partition_key=PartitionKey("/id")
)