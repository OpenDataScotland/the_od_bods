#!/usr/bin/env python3

from github import Github, GithubException, GithubIntegration
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import csv
import os

GITHUB_REPO = 'OpenDataScotland/the_od_bods'

github_access_token = os.environ.get('GITHUB_ACCESS_TOKEN')
github_user_assignee = os.environ.get('GITHUB_USER_ASSIGNEE')

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
    issue_label = repo.get_label('broken link')

    open_issues = repo.get_issues(state='open', labels=[issue_label])
    
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
            except (HTTPError, URLError) as e:
                issue_body = '**Broken URL:** [#{}]({})\n\n'.format(
                    row['Source URL'], row['Source URL'])
                # Create an issue on GitHub
                issue_title = 'Broken URL for {}'.format(row['Name'])

                # Has an issue already been raised?
                exists = False
                for issue in open_issues:
                    if issue.title == issue_title:
                        exists = True
                        break

                if exists == False:                
                    new_issue = repo.create_issue(title=issue_title, assignee=github_user_assignee, body=issue_body, labels=[issue_label])
                    to_do_column.create_card(content_id=new_issue.id, content_type='Issue')
                    print(new_issue)
            else:
                issue_body = '**Broken URL:** [#{}]({})\n\n'.format(
                    row['Source URL'], row['Source URL'])
                # Close an issue if open for previously broken URL
                issue_title = 'Broken URL for {}'.format(row['Name'])

                for issue in open_issues:
                    if issue.title == issue_title:
                        issue.create_comment("Automatically closed due to URL now working.")
                        issue.edit(state='closed')
                        break

except GithubException as err:
    print('Github: Connect: error {}', format(err.data))