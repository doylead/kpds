import psycopg2
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone

yt_api_key = environ['YT_API_KEY']
channel_list_file = open('channels_aug132019.csv')

channel_list = list(filter(None,channel_list_file.read().split('\n')))
nchannels = len(channel_list) - 1 # Includes header row

connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

for i in range(1,nchannels+1): # Because of how Python handles range()
    _ , youtube_channel_external_key = channel_list[i].split(',')

    base_url_1 = ("https://www.googleapis.com/youtube/v3/channels"
            "?id=%s"
            "&key=%s"
            "&part=snippet")

    q1 = base_url_1%(youtube_channel_external_key,yt_api_key)
    r1 = requests.get(q1)
    j1 = json.loads(r1.text)

    ## This produces a playlist ID that includes all uploads for that channel ID
    ji = j1['items'][0]
    ki = ji['snippet'].keys()

    channel_title = ji['snippet']['title']
    channel_description = ji['snippet']['description']
    published_datetime = ji['snippet']['publishedAt']
    discovered_datetime = datetime.now(timezone.utc)
    tracking = False

    if 'customUrl' in ki:
        channel_custom_url = ji['snippet']['customUrl']
        insertstring = ('INSERT INTO "YouTube_Channels" '
        '(published_datetime,discovered_datetime,channel_title,channel_custom_url,channel_description,youtube_channel_external_key,tracking) '
        'values (%s,%s,%s,%s,%s,%s,%s)')
        line_list = (published_datetime,discovered_datetime,channel_title,channel_custom_url,channel_description,youtube_channel_external_key,tracking)
    else:
        insertstring = ('INSERT INTO "YouTube_Channels" '
        '(published_datetime,discovered_datetime,channel_title,channel_description,youtube_channel_external_key,tracking) '
        'values (%s,%s,%s,%s,%s,%s)')
        line_list = (published_datetime,discovered_datetime,channel_title,channel_description,youtube_channel_external_key,tracking)
    cur.execute(insertstring,line_list)

conn.commit()
cur.close()
conn.close()

