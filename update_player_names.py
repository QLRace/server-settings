#!/usr/bin/env python3.5
'''
Updates a players name using the steam api and pushes it to 'minqlx:player:<steamid>'.
'''

import redis
import requests
import os
import sys

r = redis.StrictRedis(unix_socket_path='/var/run/redis/redis.sock')
url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}'

if 'STEAM_API_KEY' in os.environ:
    url = url.format(os.environ['STEAM_API_KEY'])
else:
    print('STEAM_API_KEY environment variable is not set!')
    sys.exit()

for key in r.sscan_iter('minqlx:players'):
    steam_id = key.decode('UTF-8')
    print(steam_id, end=",", flush=True)

    response = requests.get('{}&steamids=[{}]'.format(url, steam_id)).json()['response']
    name = response['players'][0]['personaname']
    names_key = 'minqlx:players:{}'.format(steam_id)
    current_name = r.lindex(names_key, 0)
    if current_name is not None and current_name.decode('UTF-8') != name:
        r.lrem(names_key, 0, name)
        r.lpush(names_key, name)
    r.ltrim(names_key, 0, 19)
