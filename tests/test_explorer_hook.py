from unittest.mock import patch

import pytest
import requests
from utils import MockedResponse

from airflow.exceptions import AirflowBadRequest
from airflow.models.connection import Connection
from hooks.explorer import ExplorerHook


class TestExplorerHook:
    def setup_method(self):
        self.connection = Connection(
            host="https://api.test-explorer.io", password="apikey"
        )

        class UnitTestExplorerHook(ExplorerHook):
            conn_name_attr: str = "test_conn_id"

        self.hook = UnitTestExplorerHook(connection=self.connection)

    @patch("requests.get", return_value=MockedResponse(status_code=404, json_data={}))
    def test_api_request_failed(self, patched_req):
        self.setup_method()
        with pytest.raises(requests.exceptions.HTTPError):
            self.hook.api_request(module="test_module", action="test_action")
        patched_req.assert_called()

    @patch(
        "requests.get",
        return_value=MockedResponse(
            status_code=200, json_data={"status": "0", "message": "", "result": ""}
        ),
    )
    def test_api_request_failed_with_response(self, patched_req):
        self.setup_method()
        with pytest.raises(AirflowBadRequest):
            self.hook.api_request(module="test_module", action="test_action")
        patched_req.assert_called()

    @patch(
        "requests.get",
        return_value=MockedResponse(
            status_code=200, json_data={"status": "1", "result": "success"}
        ),
    )
    def test_api_request_success(self, patched_req):
        self.setup_method()
        res = self.hook.api_request(module="test_module", action="test_action")
        patched_req.assert_called()
        assert res == "success"
