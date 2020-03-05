#!/usr/bin/env python3

'''
The purpose of this script is to query the YouTube API for the number
of views, likes, dislikes, and comments on a selection of YouTube
videos and to store that information in a SQL server
'''

import psycopg2
from psycopg2.extras import execute_values
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone
from isodate import parse_duration
from sys import argv
from utilities import unpack_video_ts_json,flatten_list,segment_list

script_start_time = datetime.now()

yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

### This script to be called by CRON - Check scheduling!

### What videos will we be working with?
channel_query = ('SELECT youtube_video_external_key '
                    'FROM "YouTube_Videos" '
                    'WHERE stats_tracking=\'t\' AND stats_frequency=15;')
cur.execute(channel_query)
video_results = cur.fetchall()

### Format queries for YouTube API
flat_video_results = flatten_list(video_results)
segmented_video_results = segment_list(flat_video_results,50)

for video_id in flat_video_results:
    

for segment in segmented_video_results:
    composite_key = ",".join(segment)
    ## We now have composite keys of, at max, 50 entries (YT API Limit)

    composite_key = ",".join(segment)
    dt_now = datetime.now(timezone.utc)
    base_url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=%s&key=%s'
    query_url = base_url%(composite_key, yt_api_key)
    r = requests.get(query_url)
    parsed_json = json.loads(r.text)

    ## Data order is
    ##    [timestamp, numViews, numLikes, numDislikes, numComments, numFavorites]
    parsed = unpack_video_ts_json(parsed_json,dt_now)

### Store in SQL



