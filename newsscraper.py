'''
Reddit News Scraper -  get top X articles from various news subreddits
'''
import praw, sys

from pathlib import Path
import configparser


def main():
    credpath = str(Path.home()) + '/credentials.txt'
    creds = configparser.ConfigParser()
    creds.read(credpath)
    # check if provided creds exist blank
    for entry in creds['reddit']:
        if creds['reddit'][entry].isspace():
            sys.exit('ERROR: No credentials found')

    with praw.Reddit(client_id=creds['reddit']['client_id'], client_secret=creds['reddit']['client_secret'],
                     user_agent=creds['reddit']['user_agent'], username=creds['reddit']['username'],
                     password=creds['reddit']['password']) as rclient:
        try:
            # try auth
            rclient.user.me()
        except:
            print('failed')
            sys.exit()
    news_subreddits = rclient.subreddit('news+worldnews')
    topofsub = news_subreddits.top(limit=10)
    for sub in topofsub:
        print('Title: ' + sub.title, '\nSubreddit Name: ' + sub.id)


if __name__ == '__main__':
    main()
