import json
import secrets

from requests.exceptions import HTTPError
from eth_account import Account

class MockedResponse:
    def __init__(self, status_code: int, json_data: dict):
        self.status_code = status_code
        self.text = json.dumps(json_data)

    def raise_for_status(self):
        if self.status_code >= 400 and self.status_code <= 500:
            raise HTTPError()

    def json(self):
        return json.loads(self.text)

def random_address():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    return Account.from_key(private_key).address