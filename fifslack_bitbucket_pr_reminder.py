#!/usr/bin/env python
# coding: utf-8

from fifbucket.client import Bitbucket
from slackclient import SlackClient
import os
import sys
import pendulum

SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#general')
REPOS = tuple(
    os.environ.get('REPOS', '').split(','),
)
PROJECTS = tuple(
    os.environ.get('PROJECTS', '').split(','),
)
IGNORE_REPOS = tuple(
    os.environ.get('IGNORE_REPOS', '').split(','),
)
HOURS = os.environ.get('HOURS')
try:
    HOURS = int(HOURS)
except Exception:
    HOURS = None

try:
    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    BITBUCKET_USER = os.environ['BITBUCKET_USER']
    BITBUCKET_PASSWORD = os.environ['BITBUCKET_PASSWORD']
    OWNER = os.environ['OWNER']
except KeyError as error:
    sys.stderr.write('Please set the environment variable {0}'.format(error))
    sys.exit(1)

INITIAL_MESSAGE = """\
Hi! There's a few open pull requests you should take a \
look at:

"""


def get_pr_info(repository):
    lines = []
    if IGNORE_REPOS[0]:
        if repository in IGNORE_REPOS:
            return lines
    bitbucket = Bitbucket(
        owner=OWNER, username=BITBUCKET_USER, password=BITBUCKET_PASSWORD)
    pull_requests = bitbucket.get_pr(repository)
    now = pendulum.now()
    if pull_requests['size'] > 0:
        for pr in pull_requests['values']:
            html_url = pr['links']['html']['href']
            title = pr['title']
            creator = pr['author']['username']
            updated_on = pendulum.parse(pr['updated_on'])
            if HOURS == None:
                line = '*[{0}]* <{1}|{2} - by {3}>'.format(
                    repository, html_url, title, creator)
                lines.append(line)
            else:
                if now.subtract(hours=HOURS) >= updated_on:
                    line = '*[{0}]* <{1}|{2} - by {3}> ({4}) {5}'.format(
                        repository, html_url, title, creator, updated_on.diff_for_humans(), updated_on)
                    lines.append(line)
    return lines


def format_pull_requests():
    bitbucket = Bitbucket(
        owner=OWNER, username=BITBUCKET_USER, password=BITBUCKET_PASSWORD)
    lines = []

    if PROJECTS[0]:
        for project in PROJECTS:
            for repo in bitbucket.get_repos_all(query='project.key="{}"'.format(project)):
                lines = lines + get_pr_info(repo['slug'])
    if REPOS[0]:
        for repo in REPOS:
            lines = lines + get_pr_info(repo)
    return lines


def send_to_slack(text):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)
    sc.api_call(
        "chat.postMessage",
        username='Pull Request Reminder',
        icon_emoji=':bell:',
        channel=SLACK_CHANNEL,
        text=text
    )


def cli():
    lines = format_pull_requests()
    if lines:
        text = INITIAL_MESSAGE + '\n'.join(lines)
        send_to_slack(text)


if __name__ == '__main__':
    cli()
