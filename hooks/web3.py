import json
import logging
from copy import deepcopy
from typing import Any

import requests
from web3 import Web3

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection

logging.basicConfig(level=logging.INFO)

ETHERSCAN_API = "https://api.etherscan.io/api"
SNOWTRACE_API = "https://api.snowtrace.io/api"
FTMSCAN_API = "https://api.ftmscan.com/api"
ARBISCAN_API = "https://api.ftmscan.com/api"
BSCSCAN_API = "https://api.bscscan.com/api"
OPTIMISTIC_ETHERSCAN_API = "https://api-optimistic.etherscan.io/api"
POLYGONSCAN_API = "https://api.polygonscan.com/api"
MOONSCAN_API = "https://api.moonscan.com/api"


class Web3Hook(BaseHook):
    """Interact with web3"""

    conn_name_attr: str = "web3_conn_id"
    conn_type: str = "web3"
    hook_name: str = "Web3"
    default_conn_name: str = "web3"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.conn_name_attr:
            raise AirflowException("conn_name_attr is not defined")
        elif len(args) == 1:
            setattr(self, self.conn_name_attr, args[0])
        elif self.conn_name_attr not in kwargs:
            setattr(self, self.conn_name_attr, self.default_conn_name)
        else:
            setattr(self, self.conn_name_attr, kwargs[self.conn_name_attr])
        self.connection: Connection | None = kwargs.pop("connection", None)
        self.explorer: str | None = kwargs.pop("scanner", None)
        self.conn: Web3 = None

    def get_conn(self) -> Any:
        conn_id = getattr(self, self.conn_name_attr)
        conn = deepcopy(self.connection or self.get_connection(conn_id))
        self.conn = Web3(Web3.HTTPProvider(conn.host))

    def toChecksumAddress(self, address: str) -> str:
        return Web3.toChecksumAddress(address)

    def _fetch_abi(self, address: str) -> list:
        checksumAddress = self.toChecksumAddress(address=address)
        response = requests.get(
            f"{self.explorer}?module=contract&action=getabi&address={checksumAddress}"
        )
        response_json = response.json()
        abi_json = json.loads(response_json["result"])
        return abi_json
