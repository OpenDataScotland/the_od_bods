#!/usr/bin/env python3

from github import Github, GithubException, GithubIntegration
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import csv
import os

github_access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
GITHUB_REPO = 'OpenDataScotland/the_od_bods'
GITHUB_USER_ASSIGNEE = 'AndrewSage'

try:
    git = Github(github_access_token)
    repo = git.get_repo(GITHUB_REPO)
    
    # Get the project's 'To do' column
    projects = repo.get_projects()
    project = projects[0]
    project_columns = project.get_columns()
    to_do_column = None
    for project_column in project_columns:
        if project_column.name == 'To do':
            to_do_column = project_column
            break

    with open('../sources.csv', 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:

            req = Request(
                row['Source URL'])
            try:
                response = urlopen(req)
            except HTTPError as e:
                print('{} server couldn\'t fulfill the request {} : {}'.format(
                    row['Name'], row['Source URL'], e.code))
            except URLError as e:
                print('{} failed {} : {}'.format(
                    row['Name'], row['Source URL'], e.reason))
                issue_body = '**Broken URL:** [#{}]({})\n\n'.format(
                    row['Source URL'], row['Source URL'])
                # Create an issue on GitHub
                issue_title = 'Broken URL for {}'.format(row['Name'])
                # Get the repo's 'broken link' issue tag
                issue_label = repo.get_label('broken link')
                new_issue = repo.create_issue(title=issue_title, assignee=GITHUB_USER_ASSIGNEE, body=issue_body, labels=[issue_label])
                to_do_column.create_card(content_id=new_issue.id, content_type='Issue')
                # print(new_issue)
            else:
                print('{} working fine'.format(row['Name']))

except GithubException as err:
    print('Github: Connect: error {}', format(err.data))