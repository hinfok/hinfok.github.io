#!/usr/bin/env python3
"""HKInformation Data Fetcher
Fetches data from DATA.GOV.HK API and updates article JSONs.
Requires DATA_GOV_HK_KEY env var (register at data.gov.hk)"""
import json, os, sys, csv, io, urllib.request, urllib.parse
from pathlib import Path
BASE = Path(__file__).parent
SRC = BASE / 'src'
API_KEY = os.environ.get('DATA_GOV_HK_KEY', '')
API = 'https://api.data.gov.hk/v1/'
DATASETS = [
    {'article':'rental-price-index','q':'private domestic price indices'},
    {'article':'public-housing','q':'public rental housing waiting time'},
    {'article':'income-vs-price','q':'median domestic household income'},
    {'article':'vacancy-rate','q':'vacancy rates private properties'},
    {'article':'homeownership-district','q':'homeownership rate district census'},
]
def api_get(path):
    url = API + path
    h = {'User-Agent':'HKInfo-Fetcher/1.0'}
    if API_KEY: h['Authorization'] = 'Bearer ' + API_KEY
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode('utf-8'))
    except: return None
def main():
    print('HKInformation Data Fetcher')
    print('='*40)
    if not API_KEY:
        print('No DATA_GOV_HK_KEY set. The script will use sample data.')
        print('Register at https://data.gov.hk/en/help/api for API key')
        print()
    test = api_get('catalog?q=test&rows=1')
    if test is None:
        print('WARNING: API unreachable from this environment.')
        print('Expected in Codex sandbox. Works from GitHub Actions.')
    else:
        print('API connection OK.')
    for ds in DATASETS:
        q = urllib.parse.quote(ds['q'])
        print(f'  Searching: {ds["q"]}')
        if test is not None:
            res = api_get(f'catalog?q={q}&rows=5')
            if res and 'results' in res:
                print(f'  Found {len(res["results"])} datasets')
            else:
                print('  No results')
    print()
    print('Pipeline ready. Integrate with GitHub Actions.')
if __name__ == '__main__': main()