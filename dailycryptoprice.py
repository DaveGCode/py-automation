#!/usr/bin/env python3
'''
DailyCryptoPrice.py -> scrape and display current and historical market price of X cryptocurrency
'''

import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta


def main():
    site_info = requests.get('https://coinmarketcap.com/')
    site = bs(site_info.content, 'html.parser')

    # Scrape for js script crypto coin info --> <script id="__NEXT_DATA__" type="application/json">
    data = site.find('script', id='__NEXT_DATA__', type='application/json')
    coin_info = json.loads(data.contents[0])
    coin_listings = coin_info['props']['initialState']['cryptocurrency']['listingLatest']['data']
    '''Ex."data":[{"id":1,"name":"Bitcoin","symbol":"BTC","slug":"bitcoin","max_supply":21000000,"circulating_supply":18599468,"total_supply":18599468,
    "last_updated":"2021-01-13T18:49:02.000Z","quote":{"USD":{"price":35744.83634971195,
    "volume_24h":65855703937.84699,"percent_change_1h":3.02258498,"percent_change_24h":2.74950539,
    "percent_change_7d":1.92688419,"market_cap":664834939851.7042,"last_updated":"2021-01-13T18:49:02.000Z"}},
    "rank":1,"noLazyLoad":true}' '''

    # todo get slug key from coin info
    coins = {}

    startdate = str(datetime.today())
    enddate = str(datetime.today() - timedelta(days=1))
    for coin in coins:
        page = requests.get(
            f'https://coinmarketcap.com/currencies/{coins[coin]}/historical-data/?start={startdate}&end={enddate}')


if __name__ == '__main__':
    main()
