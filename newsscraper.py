#!/usr/bin/env python3
'''
Reddit News Scraper -  get top X articles from various news subreddits for past day
'''

import praw, sys, pandas
from praw import exceptions
from pathlib import Path
import configparser


def get_credentials(service):
    credpath = str(Path.home()) + '/credentials.txt'
    creds = configparser.ConfigParser()
    creds.read(credpath)
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
        except ValueError:
            print('ERROR: Invalid credentials provide4d')
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
    return thread_data


def main():
    creds = get_credentials('reddit')
    rclient = reddit_client_setup(creds)
    news = get_news(rclient)
    print(news)


if __name__ == '__main__':
    main()
