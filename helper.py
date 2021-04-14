import getopt
import sys
import requests
from pathlib import Path

def get_opts():
    aopts = getopt.getopt(sys.argv[1:], '', ['username=', 'password=', 'endpoint='])

    opts = {}
    for opt in aopts[0]:
        if opt[0].startswith('--'):
            opts[opt[0][2:]] = opt[1]
        else:
            opts[opt[0]] = opt[1]
    return opts

def get_all_items(url, auth=None):
    current_url = url
    items = []
    hasMore = True
    offset = 0
    while hasMore:
        response = requests.get(current_url, auth=auth)
        content = response.json()
        items = [*items, *content['items']]
        hasMore = content['hasMore']
        if hasMore:
            offset += content['count']
            current_url = url + '?offset=' + str(offset)
    return items

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)