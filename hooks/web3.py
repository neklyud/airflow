from typing import Any
from airflow.hooks.base import BaseHook
from airflow.models.connection import Connection
from web3 import Web3
from copy import deepcopy
from airflow.exceptions import AirflowException
from functools import cached_property    
from typing import Optional, Sequence, Callable
from web3.contract import Contract


class Web3Hook(BaseHook):
    """Interact with web3"""

    def __init__(self, *args, **kwargs):
        self.conn_id: str | None = kwargs.pop('conn_id', None)
        self.connection: Connection | None = kwargs.pop("connection", None)
        self._w3: Web3 | None = kwargs.pop('web3', None)
        self._middlewares: Sequence[Any] | None = kwargs.pop('middlewares', None)

    def get_conn(self) -> Connection:
        return self.get_connection(self.conn_id)

    @cached_property
    def w3(self) -> Web3:
        conn = deepcopy(self.connection or self.get_connection(self.conn_id))
        self._w3 = Web3(provider=Web3.HTTPProvider(conn.host), middlewares=self._middlewares)
        return self._w3
    
    def get_contract(self, address: str, abi: Any) -> Contract:
        return self.w3.eth.contract(address=address, abi=abi)
    

class Web3ContractHook(Web3Hook):
    def __init__(self, address: str, abi: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address: str = Web3.toChecksumAddress(address)
        self.abi: Any = abi
        self.contract = self.get_contract(self.address, self.abi)


    def event_callback(self, name: str) -> Callable:
        def inner(from_block: int, to_block: int, *args, **kwargs):
            filters = kwargs.get('filters', None)
            block_hash = kwargs.get('block_hash', None)
            return self.contract.events[name].getLogs(filters, from_block, to_block, block_hash)
        return inner
    
    def contract_function_callback(self, function: str) -> Callable:
        def inner(block: int | str = 'latest', *args, **kwargs):
            return self.contract.functions[function].call(block_identifier=block, *args, **kwargs)
        return inner

    def __getattr__(self, name: str):
        contract_functions = [func.function_identifier for func in self.contract.all_functions()]
        if name in contract_functions:
            return self.contract_function_callback(name)
        if name in self.contract.events:
            return self.event_callback(name=name)
        raise AttributeError('Action not found')