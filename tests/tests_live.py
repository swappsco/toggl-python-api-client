import unittest
import json
from toggl.api_client import TogglClientApi


class TogglClientApiLiveTests(unittest.TestCase):

    api = None

    # Runs before *every* tests
    def setUp(self):
        file_contents = open("tests_live_config.json")
        self.settings = json.load(file_contents)
        file_contents.close()

        self.api = TogglClientApi(self.settings)

    # Runs after *every* tests
    def tearDown(self):
        del self.api

    def test_api_client_instance_created(self):
        self.assertNotEqual(self.api, None)

    def test_valid_toggl_base_url(self):
        self.assertEqual(self.api.api_base_url, "https://api.track.toggl.com/api/v8")

    def test_api_toggl_auth_check_response_ok(self):
        response = self.api.query("/me")
        self.assertEqual(response.status_code, 200)

    def test_api_toggl_get_list_of_workspaces_response_ok(self):
        response = self.api.get_workspaces()
        self.assertEqual(response.status_code, 200)

    def test_api_toggl_get_workspace_by_name_found(self):
        workspace = self.api.get_workspace_by_name(self.settings["workspace_name"])
        self.assertNotEqual(workspace["id"], "")

    def test_api_toggl_get_workspace_members_response_ok(self):
        workspace = self.api.get_workspace_by_name(self.settings["workspace_name"])
        response = self.api.get_workspace_members(workspace["id"])
        self.assertEqual(response.status_code, 200)

    def test_api_toggl_get_member_total_hours_range_response_ok(self):
        workspace_id = self.settings["workspace_id"]
        user_id = self.settings["user_id"]
        start_date = self.settings["start_date"]
        end_date = self.settings["end_date"]
        total = self.api.get_user_hours_range(
            "toggl-python-api-client-nosetests",
            workspace_id,
            user_id,
            start_date,
            end_date,
        )

        self.assertGreater(total, 0)
