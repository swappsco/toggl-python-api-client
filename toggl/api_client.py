import requests


class TogglClientApi(object):

    defaultCredentials = {
        "username": "",
        "workspace_name": "",
        "base_url": "https://api.track.toggl.com/api",
        "ver_api": 8,
        "base_url_report": "https://api.track.toggl.com/reports/api",
        "ver_report": 2,
    }
    credentials = {}
    api_token = ""
    api_username = ""
    api_base_url = None
    api_report_base_url = None
    workspace_name = None
    requests = None

    def __init__(self, credentials):
        credentials.update(self.defaultCredentials)
        self.credentials = credentials
        self.api_base_url = self.build_api_url(
            self.credentials["base_url"], self.credentials["ver_api"]
        )
        self.api_report_base_url = self.build_api_url(
            self.credentials["base_url_report"], self.credentials["ver_report"]
        )
        self.api_token = self.credentials["token"]
        self.timeout = self.credentials.get("timeout", 60)
        self.api_username = self.credentials["username"]
        self.user_agent = self.credentials["user_agent"]
        self.workspace_id = int(self.credentials["workspace_id"])
        return

    @staticmethod
    def build_api_url(base_url, version):
        return base_url + "/v" + str(version)

    def get_workspace_by_name(self, name):
        workspace_found = None
        list_response = self.get_workspaces()

        if list_response.status_code != requests.codes.ok:
            list_response.raise_for_status()

        workspace_list = list_response.json()
        for workspace in workspace_list:
            if workspace["name"] == name:
                workspace_found = workspace

        return workspace_found

    def get_workspaces(self):
        return self.query("/workspaces")

    def get_projects(self):
        return self.query("/workspaces/%i/projects" % self.workspace_id)

    def get_workspace_members(self, workspace_id):
        response = self.query("/workspaces/" + str(workspace_id) + "/workspace_users")
        return response

    """
    @param start_date YYYY-MM-DD
    @param end_date YYYY-MM-DD
    """ ""

    def get_user_hours_range(
        self, user_agent, workspace_id, user_id, start_date, end_date
    ):
        params = {
            "workspace_id": workspace_id,
            "since": start_date,
            "until": end_date,
            "user_agent": user_agent,
            "user_ids": user_id,
            "grouping": "users",
            "subgrouping": "projects",
        }
        projects_worked_response = self.query_report("/summary", params)

        if projects_worked_response.status_code != requests.codes.ok:
            projects_worked_response.raise_for_status()

        json_response = projects_worked_response.json()

        if len(json_response["data"]) > 0:
            time_total = json_response["data"][0]["time"]
        else:
            time_total = 0

        return time_total

    """
    @param start_date datetime.date()
    @param end_date datetime.date()
    """

    def get_project_times(self, project_id, start_date, end_date, extra_params={}):
        params = {
            "workspace_id": self.workspace_id,
            "project_ids": project_id,
            "since": start_date.strftime("%Y-%m-%d"),
            "until": end_date.strftime("%Y-%m-%d"),
            "user_agent": self.user_agent,
            "grouping": "users",
            "subgrouping": "projects",
        }
        params.update(extra_params)
        time_entries_response = self.query_report("/details", params)

        if time_entries_response.status_code != requests.codes.ok:
            time_entries_response.raise_for_status()

        json_response = time_entries_response.json()

        return json_response

    def get_dashboard_data(self, params={}):
        dashboard_response = self.query("/dashboard/%i" % self.workspace_id, params)

        if dashboard_response.status_code != requests.codes.ok:
            dashboard_response.raise_for_status()

        json_response = dashboard_response.json()

        return json_response

    def create_time_entry(self, json_data):
        """
        creates a time entry. data should have
        this structure
        {
            "time_entry": {
                "description":"<description>",
                "tags":[<list-of-tags>],
                "duration":<duration-in-seconds>,
                "start":"<iso8601-format-datetime>",
                "pid":<project-id>,
                "created_with":"<name-of-your-client-app>"
            }
        }
        """
        response = self.query("/time_entries", method="POST", json_data=json_data)

        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        response = response.json()

        return response

    def query_report(self, url, params={}, method="GET"):
        return self._query(self.api_report_base_url, url, params, method)

    def query(self, url, params={}, method="GET", json_data={}):
        return self._query(self.api_base_url, url, params, method, json_data)

    def _query(self, base_url, url, params, method, json_data={}):
        api_endpoint = base_url + url
        toggl_auth = (self.api_token, "api_token")
        toggl_headers = {"content-type": "application/json"}

        if method == "POST":
            response = self._do_post_query(
                api_endpoint,
                headers=toggl_headers,
                auth=toggl_auth,
                params=params,
                timeout=self.timeout,
                json_data=json_data,
            )
        elif method == "GET":
            response = self._do_get_query(
                api_endpoint,
                headers=toggl_headers,
                auth=toggl_auth,
                params=params,
                timeout=self.timeout,
            )
        else:
            response = self._do_get_query(
                api_endpoint,
                headers=toggl_headers,
                auth=toggl_auth,
                params=params,
                timeout=self.timeout,
            )

        return response

    @staticmethod
    def _do_get_query(url, headers, auth, params, timeout):
        response = requests.get(
            url, headers=headers, auth=auth, params=params, timeout=timeout
        )

        return response

    @staticmethod
    def _do_post_query(url, headers, auth, params, timeout, json_data):
        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=json_data,
            params=params,
            timeout=timeout,
        )

        return response
