# -*- coding: utf-8 -*-

import requests
import json
import sys
import time

API_KEY = 'AIzaSyAvSimua5gSCK4HJHc4Lt2mdwlMmkgVm-Q'
BASE_URL = 'https://www.googleapis.com/youtube/v3'
CHANNEL_ID = sys.stdin.readline()
request_num = 0

# 1回目
first_url = BASE_URL + \
    '/search?part=snippet&channelId=%s&key=%s&maxResults=50&type=video&order=date'
base_res = requests.get(first_url % (CHANNEL_ID, API_KEY))
request_num += 1
base_res_json = base_res.json()
if 'nextPageToken' in base_res_json:
    next_page_token = base_res_json['nextPageToken']
    # 2回目以降
    from_second_url = BASE_URL + \
        '/search?part=snippet&channelId=%s&key=%s&maxResults=50&type=video&order=date&pageToken=%s'
    while True:
        res = requests.get(from_second_url % (
            CHANNEL_ID, API_KEY, next_page_token))
        time.sleep(1)
        request_num += 1
        res_json = res.json()
        base_res_json['items'] += res_json['items']
        if 'nextPageToken' in res_json:
            next_page_token = res_json['nextPageToken']
        else:
            break


print(json.dumps(base_res_json))


'''
lengths_url = BASE_URL + '/videos?part=contentDetails&id=%s&key=%s'
videos_res = requests.get(videos_url % (CHANNEL_ID, API_KEY))
lengths = []

if videos_res.status_code != 200:
    print('存在しないチャンネルのため、動画をインサートできませんでした')
else:
    while True:
        videos_res = requests.get(videos_url % (CHANNEL_ID, API_KEY))
        quota_used += 5
        videos_result = videos_res.json()

        for video in videos_result['items']:
            try:
                lengths.append(
                    video['contentDetails']['upload']['videoId'])
            except:
                pass

        lengths_res = requests.get(
            lengths_url % (','.join(lengths), API_KEY))
        quota_used += 3
        lengths_result = lengths_res.json()

        for video, length in zip(videos_result['items'], lengths_result['items']):
            try:
                data = (None, CHANNEL_ID, video['contentDetails']['upload']['videoId'], video['snippet']
                        ['title'], thum, video['snippet']['publishedAt'], length['contentDetails']['duration'])
                cur.execute(video_sql, data)
                conn.commit()
            except:
                pass
        try:
            final_video = videos_result['items'][49]['snippet']['publishedAt']
            videos_url = BASE_URL + \
                '/activities?part=snippet,contentDetails&channelId=%s&key=%s&maxResults=50&     =' + final_video
            lengths.clear()
        except:
            print('動画インサート完了')
            print(quota_used)
            break
'''
