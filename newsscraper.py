'''
Reddit News Scraper -  get top X articles from various news subreddits
'''
import praw, sys, pandas

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
    thread_info = { "title":[],
                "score":[],
                "id":[], "url":[],
                "comms_num": [],
                "created": [],
                "body":[]}
    topofsub = news_subreddits.top(limit=10)
    for thread in topofsub:
        thread_info['title'].append(thread.title)
        thread_info['score'].append(thread.score)
        thread_info['id'].append(thread.id)
        thread_info['url'].append(thread.url)
        thread_info['comms_num'].append(thread.num_comments)
        thread_info['created'].append(thread.created)
        thread_info['body'].append(thread.selftext)
    thread_data = pandas.DataFrame(thread_info)
    print(thread_data)


if __name__ == '__main__':
    main()
