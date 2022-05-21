# Alive

Raises a GitHub issue for any URL in `../sources.csv` that is not responding.

To run it requires a GitHub Access Token to be set in the environment variable `GITHUB_ACCESS_TOKEN`.

Set `GITHUB_USER_ASSIGNEE` to the user that will be automatically assigned the issue.


Run via `GITHUB_ACCESS_TOKEN='<token>' ./alive.py`