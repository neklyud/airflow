from airflow.models.baseoperator import BaseOperator
from hooks.web3 import Web3Hook
from typing import Any

class Web3(BaseOperator):
    def __init__(self, rpc_conn_id: str, **kwargs):
        super().__init__(**kwargs)
        self.rpc_conn_id: str = rpc_conn_id
    
    def execute(self, context) -> Any:
        hook = Web3Hook(web3_conn_id=self.rpc_conn_id)
        return super().execute(context)