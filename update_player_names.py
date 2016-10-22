#!/usr/bin/env python3.5
'''
Updates a players name using the steam api and sets 'minqlx:player:<steam_id>' to [<name>].
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
    print('minqlx:player:{}'.format(steam_id))

    response = requests.get('{}&steamids=[{}]'.format(url, steam_id)).json()['response']
    name = response['players'][0]['personaname']
    names_key = 'minqlx:players:{}'.format(steam_id)
    r.lpush(names_key, name)
    r.ltrim(names_key, 0, 0)
