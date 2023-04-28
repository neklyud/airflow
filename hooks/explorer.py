import requests
from web3 import Web3

from airflow.exceptions import AirflowBadRequest
from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection


class ExplorerHook(BaseHook):
    default_conn_name = "explorer_default"
    conn_type: str = "explorer"
    hook_name: str = "Explorer"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.conn_id: str | None = kwargs.get("conn_id", None)
        self.connection: Connection | None = kwargs.get("connection", None)
        self.apikey: str | None = None

    def api_request(self, module: str, action: str, **params):
        if not self.connection:
            self.connection = self.get_connection(self.conn_id)
        if not self.apikey:
            self.apikey = self.connection.password

        params["module"] = module
        params["action"] = action
        params["apikey"] = self.apikey

        response = requests.get(self.connection.host, params=params)
        response.raise_for_status()
        results = response.json()
        if results["status"] != "1":
            raise AirflowBadRequest(
                f'{results["message"]}, results:\n{results["result"]}'
            )
        return results["result"]
