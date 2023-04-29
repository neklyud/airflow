import pytest
from airflow.models.connection import Connection
from hooks.web3 import Web3Hook, Web3ContractHook
from utils import random_address
from typing import Optional
from unittest.mock import patch
import web3

def get_abi():
    return '''
        [
            {
                "constant": true,
                "inputs": [],
                "name": "test_function",
                "outputs": [
                    {
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "payable": false,
                "stateMutability": "view",
                "type": "function"
            }
        ]
        '''

class TestWeb3Hook:
    def setup_method(self):
        self.connection: Connection = Connection(host='test-host')
        self.hook = Web3Hook(connection=self.connection)

    def test__w3(self):
        self.setup_method()
        w3 = self.hook.w3
        assert w3.provider.endpoint_uri == self.connection.host


    def test_get_contract(self):
        self.setup_method()
        test_abi = get_abi()
        test_contract = self.hook.get_contract(address=random_address(), abi=test_abi)
        assert len(test_contract.all_functions()) > 0


class TestWeb3ContractHook:
    def setup_method(self):
        self.connection: Connection = Connection(host='test-host')
        contract_address = random_address()
        abi = get_abi()
        self.hook = Web3ContractHook(connection=self.connection, address=contract_address, abi=abi)

    def test_contract_function_callback(self):
        self.setup_method()
        callback = self.hook.contract_function_callback('test_function')
        assert callable(callback)

    def test_event_callback(self):
        self.setup_method()
        callback = self.hook.event_callback('event')
        assert callable(callback)

    @patch('web3.contract.ContractFunction.call')
    def test__getattr__(self, patched_call):
        self.setup_method()
        self.hook.test_function(block=123)
        patched_call.assert_called_with(block_identifier=123)