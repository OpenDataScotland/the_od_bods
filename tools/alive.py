#!/usr/bin/env python3

import sys
from github import Github, GithubException, GithubIntegration
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import csv
import os

GITHUB_REPO = "OpenDataScotland/the_od_bods"

github_access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
github_user_assignee = os.environ.get("GITHUB_USER_ASSIGNEE")

if github_access_token == None:
    print("GITHUB_ACCESS_TOKEN needs to be defined")
    quit()

if github_user_assignee == None:
    print("GITHUB_USER_ASSIGNEE needs to be defined")
    quit()

try:
    git = Github(github_access_token)
    repo = git.get_repo(GITHUB_REPO)

    # Get the repo's 'broken link' issue label    
    issue_label = repo.get_label("broken link")

    open_issues = repo.get_issues(state="open", labels=[issue_label])

    with open("../sources.csv", "r") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:

            req = Request(row["Source URL"])
            try:
                response = urlopen(req)
                print(f"Got status code {response.getcode()} for {req.full_url}")
            except (HTTPError, URLError) as e:
                print(f"Got status code {e.code} for {req.full_url}")
                issue_body = "**Broken URL:** [#{}]({})\n\n".format(
                    row["Source URL"], row["Source URL"]
                )
                # Create an issue on GitHub
                issue_title = "Broken URL for {}".format(row["Name"])

                # Has an issue already been raised?
                exists = False
                for issue in open_issues:
                    if issue.title == issue_title:
                        exists = True
                        break

                if exists == False:
                    new_issue = repo.create_issue(
                        title=issue_title,
                        assignee=github_user_assignee,
                        body=issue_body,
                        labels=[issue_label],
                    )
                    print(new_issue)
            else:
                issue_body = "**Broken URL:** [#{}]({})\n\n".format(
                    row["Source URL"], row["Source URL"]
                )
                # Close an issue if open for previously broken URL
                issue_title = "Broken URL for {}".format(row["Name"])

                for issue in open_issues:
                    if issue.title == issue_title:
                        issue.create_comment(
                            "Automatically closed due to URL now working."
                        )
                        issue.edit(state="closed")
                        break

except GithubException as err:
    print(err)
    print("Github: Connect: error {}", format(err.data))
    sys.exit(-1)