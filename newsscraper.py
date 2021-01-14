#!/usr/bin/env python3
'''
Reddit News Scraper -  get top X articles from various news subreddits for past day
'''

import configparser
from pathlib import Path


import pandas
import praw
from requests import exceptions
import requests
import sys
from praw import exceptions


def post_to_slack(msg, url):
    if len(msg) == 0:
        sys.exit('Error: No data found')
    payload = {'news': msg}
    try:
        requests.post(url, json=payload)
    except requests.exceptions.HTTPError as e:
        raise sys.exit(e)
    except requests.exceptions.URLRequired as urle:
        raise sys.exit(urle)
    except requests.exceptions.Timeout as te:
        raise sys.exit(te)


def get_credentials(service):
    credpath = str(Path.home()) + '/credentials.txt'
    creds = configparser.ConfigParser()
    creds.read(credpath)
    if service == 'slack':
        if creds[service]['webhook_url'].isspace():
            sys.exit('ERROR: No url found')
        url = creds[service]['webhook_url']
        return url
    # check if creds are provided / are not blank
    for entry in creds[service]:
        if creds[service][entry].isspace():
            sys.exit('ERROR: No credentials found')
    return creds


def reddit_client_setup(creds):
    with praw.Reddit(client_id=creds['reddit']['client_id'], client_secret=creds['reddit']['client_secret'],
                     user_agent=creds['reddit']['user_agent'], username=creds['reddit']['username'],
                     password=creds['reddit']['password']) as rclient:
        try:
            # try auth
            rclient.user.me()
        except praw.exceptions.APIException as err:
            print(err)
            sys.exit()
    return rclient


def get_news(rclient):
    news_subreddits = rclient.subreddit('news+worldnews')
    thread_info = {"title": [],
                   "score": [],
                   "id": [], "url": [],
                   "total_comments": [],
                   "created": [],
                   "body": []}
    topofsub = news_subreddits.top(limit=10, time_filter="day")
    for thread in topofsub:
        thread_info['title'].append(thread.title)
        thread_info['score'].append(thread.score)
        thread_info['id'].append(thread.id)
        thread_info['url'].append(thread.url)
        thread_info['total_comments'].append(thread.num_comments)
        thread_info['created'].append(thread.created)
        thread_info['body'].append(thread.selftext)
    thread_data = pandas.DataFrame(thread_info)
    return thread_data.to_json()


def main():
    creds = get_credentials('reddit')
    slack_url = get_credentials('slack')
    # slack_url = 'https://hooks.slack.com/workflows/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'
    rclient = reddit_client_setup(creds)
    news = get_news(rclient)
    post_to_slack(news, slack_url)


if __name__ == '__main__':
    main()
