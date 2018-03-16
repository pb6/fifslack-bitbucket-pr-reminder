#!/usr/bin/env python
# coding: utf-8

from fifbucket.client import Bitbucket
from slackclient import SlackClient
import os
import sys

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

try:
    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    BITBUCKET_USER = os.environ['BITBUCKET_USER']
    BUTBUCKET_PASSWORD = os.environ['BUTBUCKET_PASSWORD']
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
        owner=OWNER, username=BITBUCKET_USER, password=BUTBUCKET_PASSWORD)
    pull_requests = bitbucket.get_pr(repository)
    if pull_requests['size'] > 0:
        for pr in pull_requests['values']:
            owner = 'falabellafif'
            html_url = pr['links']['html']['href']
            title = pr['title']
            creator = pr['author']['username']
            line = '*[{0}/{1}]* <{2}|{3} - by {4}>'.format(
                owner, repository, html_url, title, creator)
            lines.append(line)
    return lines


def format_pull_requests():
    bitbucket = Bitbucket(
        owner=OWNER, username=BITBUCKET_USER, password=BUTBUCKET_PASSWORD)
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
