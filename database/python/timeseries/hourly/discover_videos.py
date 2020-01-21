import psycopg2
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone

yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

### This script to be called by CRON - Check scheduling!

### Pseudocode in-line for easier development

## Query DB for channels actively being tracked at this frequency
channel_query = ('SELECT youtube_channel_id,youtube_channel_external_key '
                    'FROM "YouTube_Channels" '
                    'WHERE tracking=\'t\' AND scan_frequency=720 '
                    'ORDER BY youtube_channel_id;')
cur.execute(channel_query)
channel_results = cur.fetchall()
# Currently prints only SMTOWN, as expected

## Declare necessary logic variables

## Outer FOR loop through channels
for channel_result in channel_results:
    channel_id, external_key = channel_result
    channel_id = (channel_id,) # Format for psycopg2

    ## Query DB for videos on this channel
    video_query = ('SELECT youtube_video_id,youtube_video_external_key '
                    'FROM "YouTube_Videos" '
                    'WHERE youtube_channel_id=%s')
    cur.execute(video_query,channel_id)
    video_results = cur.fetchall()

    for r in video_results:
        print(r)

    more_videos_on_channel = True

    ## WHILE loop - are there new videos on this channel?

        ## Use API to pull the most recent five videos

        ## FOR loop over those videos

            ## IF a video is not already in the DB, add it

            ## ELSE condition for WHILE loop is false



