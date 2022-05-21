# Alive

Raises a GitHub issue for any URL in `../sources.csv` that is not responding.

The following environmental variables need to be set for this to run:

| Environmental Variable | Purpose |
| --- | --- |
| GITHUB_ACCESS_TOKEN | A valid [GitHub Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). |
| GITHUB_USER_ASSIGNEE | The GitHub username of the person who will automatically be assigned the issue. |

To run the script from the terminal:

 `GITHUB_ACCESS_TOKEN='<token>' GITHUB_USER_ASSIGNEE='<github username>' ./alive.py`