import json

from requests.exceptions import HTTPError


class MockedResponse:
    def __init__(self, status_code: int, json_data: dict):
        self.status_code = status_code
        self.text = json.dumps(json_data)

    def raise_for_status(self):
        if self.status_code >= 400 and self.status_code <= 500:
            raise HTTPError()

    def json(self):
        return json.loads(self.text)
