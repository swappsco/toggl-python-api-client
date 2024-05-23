toggl-python-api-client
=======================

[Toggl](http://toggl.com) is an "insanely simple time tracking" service.

This specific library is a Python-based REST client to interface with the Toggle API utilizing [requests](http://docs.python-requests.org/en/latest/).

This library is a pure api client to help other python apps interface with Toggl. I created this project primarily to help with a bigger internal project that I am doing at work while at the same time getting my feet wet in Python.

# Others out there

There is already a similar library, [toggl_target](https://github.com/mos3abof/toggl_target) though it is more of an application and the client api is not separate repo. Some ideas/concepts on the client api were taken from there but I had needed a client api only to help interface with my bigger app.

# Usage

## Pypi Package
    pip install python-toggl

## Manual installation
Download to a location of your choice and do the following.

```python

from toggl.api_client import TogglClientApi

settings = {
    'token': 'token',
    'user_agent': 'agent',
    'workspace_id': '####',
    'username': 'email',
}
toggl_client = TogglClientApi(settings)

response = toggl_client.get_workspaces()

```

# Dependencies

- Python 2.7 onwards
- [requests](http://docs.python-requests.org/en/latest/)

## Tests Dependencies

To run the tests, you will need the following packages

- unittest
- json
- [httpretty](https://github.com/gabrielfalcao/HTTPretty)

# Tests

Tests created under `/tests` are primarily integration tests and are not strictly unit tests. They consists of an offline and online(live) test.

## Offline

`tests/tests_offline.py`

These tests are for the logic of the api client. They do not connect to the actual Toggl servers - instead use [httpretty](https://github.com/gabrielfalcao/HTTPretty) to mock the responses. Sample responses are included in `tests/json_responses` and are based on Toggle responses for V8 of the main api and V2 of the report api.

## Online/Live

`tests/tests_live.py`

These tests are to check the connections to Toggl's API and to ensure that the client is handling the live responses from Toggl as expected.

To avoid adding sensitive data to version control, no api credentials have been included. To enable live tests,
- make a copy of `tests/tests_live_config.json.sample` as `tests/tests_live_config.json`
- update the settings on `tests/tests_live_config.json` as needed
