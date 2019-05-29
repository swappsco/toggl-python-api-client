import unittest
import httpretty
import json
from toggl.api_client import TogglClientApi


class ToogleClientApiTests(unittest.TestCase):

    api = None
    connectLive = False
    base_api_url = ""
    base_api_report_url = ""
    http_content_type = "application/json"

    # Runs before *every* tests
    def setUp(self):
        self.settings = {
            "workspace_name": "A Company",
            "token": "xxx",
            "base_url": "https://my.service/api",
            "ver_api": 8,
            "base_url_report": "https://my.service/reports/api",
            "ver_report": 2,
        }
        self.api = TogglClientApi(self.settings)
        httpretty.enable()  # enable HTTPretty so that it will monkey patch the socket module

        self.base_api_url = self.api.build_api_url(
            self.settings["base_url"], self.settings["ver_api"]
        )
        self.base_api_report_url = self.api.build_api_url(
            self.settings["base_url_report"], self.settings["ver_report"]
        )

    # Runs after *every* tests
    def tearDown(self):
        del self.api
        httpretty.disable()
        httpretty.reset()

    def load_json_file(self, location, base_path="tests/json_responses"):
        file_contents = open(base_path + "/" + location + ".json")
        json_data = json.load(file_contents)
        file_contents.close()

        return json_data

    def test_api_client_instance_created(self):
        self.assertNotEqual(self.api, None)

    def test_overriding_default_base_url_and_version_on_instance_creation(self):
        my_base_url = "http://myownapi.com"
        my_ver_no = 12
        credentials = {"base_url": my_base_url, "ver_api": my_ver_no}
        self.api = TogglClientApi(credentials)
        self.assertEqual(self.api.api_base_url, my_base_url + "/v" + str(my_ver_no))

    def test_api_token_set(self):
        self.assertNotEqual(self.api.api_token, "")

    def test_api_toggl_auth_response(self):
        expected_response_json_str = json.dumps(self.load_json_file("me"))
        httpretty.register_uri(
            httpretty.GET,
            self.base_api_url + "/me",
            body=expected_response_json_str,
            content_type=self.http_content_type,
        )
        response = self.api.query("/me")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, expected_response_json_str)

    def setup_test_api_toggl_get_workspace(self, json_file="workspaces"):
        expected_response_json_str = json.dumps(self.load_json_file(json_file))
        httpretty.register_uri(
            httpretty.GET,
            self.base_api_url + "/workspaces",
            body=expected_response_json_str,
            content_type=self.http_content_type,
        )

        return expected_response_json_str

    def test_api_toggl_get_list_of_workspaces_response(self):
        expected_response_json_str = self.setup_test_api_toggl_get_workspace()

        response = self.api.get_workspaces()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, expected_response_json_str)

    def setup_test_api_toggl_get_workspace_by_name(
        self, expected_found_index=2, json_file="workspaces"
    ):
        expected_response_json_str = self.setup_test_api_toggl_get_workspace(json_file)
        data = json.loads(expected_response_json_str)
        expected_workspace = data[expected_found_index]
        workspace = self.api.get_workspace_by_name(self.settings["workspace_name"])

        return workspace, expected_workspace

    def test_api_toggl_get_workspace_by_name_found(self):
        workspace, expected_workspace = (
            self.setup_test_api_toggl_get_workspace_by_name()
        )
        self.assertEqual(workspace["id"], expected_workspace["id"])

    def setup_test_api_toggl_get_workspace_members(self):
        workspace, expected_workspace = (
            self.setup_test_api_toggl_get_workspace_by_name()
        )

        expected_response_json_str = json.dumps(
            self.load_json_file("workspace_members")
        )
        httpretty.register_uri(
            httpretty.GET,
            self.base_api_url
            + "/workspaces/"
            + str(workspace["id"])
            + "/workspace_users",
            body=expected_response_json_str,
            content_type=self.http_content_type,
        )

        response = self.api.get_workspace_members(workspace["id"])

        return response, expected_response_json_str, workspace, expected_workspace

    def test_api_toggl_get_workspace_members_response_ok(self):
        response, expected_response_json_str, workspace, expected_workspace = (
            self.setup_test_api_toggl_get_workspace_members()
        )
        self.assertEqual(workspace["id"], expected_workspace["id"])
        self.assertEqual(response.status_code, 200)

    def test_api_toggl_get_workspace_members_response_count(self):
        response, expected_response_json_str, workspace, expected_workspace = (
            self.setup_test_api_toggl_get_workspace_members()
        )

        self.assertEqual(workspace["id"], expected_workspace["id"])

        received_data = response.json()
        expected_data = json.loads(expected_response_json_str)

        self.assertEqual(len(received_data), len(expected_data))

    def test_api_toggl_get_member_total_hours_range_response_ok_with_found_data(self):
        self.do_test_api_toggl_get_member_total_hours_range_response_ok(
            "report_user_project_hours"
        )

    def test_api_toggl_get_member_total_hours_range_response_ok_with_empty_data(self):
        self.do_test_api_toggl_get_member_total_hours_range_response_ok(
            "report_user_project_hours_null"
        )

    def do_test_api_toggl_get_member_total_hours_range_response_ok(
        self, datafile="report_user_project_hours"
    ):
        workspace, expected_workspace = (
            self.setup_test_api_toggl_get_workspace_by_name()
        )
        self.assertEqual(workspace["id"], expected_workspace["id"])

        workspace_id = workspace["id"]
        user_id = 222222
        start_date = "2014-03-03"
        end_date = "2014-03-07"
        user_agent = "toggl-python-api-client-nosetests"

        endpoint_url = (
            self.base_api_report_url
            + "/summary?"
            + "workspace_id="
            + str(workspace["id"])
            + "&since="
            + start_date
            + "&until="
            + end_date
            + "&user_agent="
            + user_agent
            + "&user_ids="
            + str(user_id)
            + "&grouping=users"
            + "&subgrouping=projects"
        )

        expected_response_json_str = json.dumps(self.load_json_file(datafile))
        httpretty.register_uri(
            httpretty.GET,
            endpoint_url,
            body=expected_response_json_str,
            content_type=self.http_content_type,
        )

        expected_response_json = json.loads(expected_response_json_str)
        if len(expected_response_json["data"]) > 0:
            expected_total = expected_response_json["data"][0]["time"]
        else:
            expected_total = 0

        total = self.api.get_user_hours_range(
            user_agent, workspace_id, user_id, start_date, end_date
        )

        self.assertEqual(total, expected_total)
