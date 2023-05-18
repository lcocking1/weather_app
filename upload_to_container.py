import json
from azure.cosmos import CosmosClient

class UploadToContainer:
    def __init__(self, container_name) -> None:
        c = open("credentials.json")
        cred = json.load(c)
        self.client = CosmosClient(
            url=cred["cosmos"]["account_url"],
            credential=cred["cosmos"]["primary_key"]
        )
        self.database_name = "cosmos_dev"
        self.container_name = container_name
        self.db_client = self.client.get_database_client(database=self.database_name)
        return None

    def load_items_to_container(self, items, id, partition_key):
        container_client = self.db_client.create_container_if_not_exists(
            id=id,
            partition_key=partition_key
        )
        container_client.upsert_item(items)