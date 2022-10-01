# -*- coding: utf-8 -*-

import requests
import json
import sys

API_KEY = 'AIzaSyAvSimua5gSCK4HJHc4Lt2mdwlMmkgVm-Q'
BASE_URL = 'https://www.googleapis.com/youtube/v3'
CHANNEL_ID = sys.stdin.readline()
quota_used = 0
url = BASE_URL + '/channels?part=snippet&id=%s&key=%s'
response = requests.get(url % (CHANNEL_ID, API_KEY))
if response.status_code == 200:
    print(json.dumps(response.json()))
else:
    print('error')
