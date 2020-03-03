#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import execute_values
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone
from isodate import parse_duration
from sys import argv
from utilities import unpack_video_discovery_json

script_start_time = datetime.now()

yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

### This script to be called by CRON - Check scheduling!

## Query DB for channels actively being tracked at this frequency
channel_query = ('SELECT youtube_channel_id,youtube_channel_external_key '
                    'FROM "YouTube_Channels" '
                    'WHERE discovery_tracking=\'t\' AND discovery_frequency=720 '
                    'ORDER BY youtube_channel_id;')
cur.execute(channel_query)
channel_results = cur.fetchall()

## Declare necessary logic variables

## Outer FOR loop through channels
for channel_result in channel_results:
    channel_id, youtube_channel_external_key = channel_result
    channel_id = (channel_id,) # Format for psycopg2

    ## Query DB for videos on this channel
    video_query = ('SELECT youtube_video_external_key '
                    'FROM "YouTube_Videos" '
                    'WHERE youtube_channel_id=%s')
    cur.execute(video_query,channel_id)
    video_results = cur.fetchall()
    prev_external_keys = [item for sublist in video_results for item in sublist]

    ## Find the uploads playlist
    base_channel_url = ("https://www.googleapis.com/youtube/v3/channels"
                "?id=%s"
                "&key=%s"
                "&part=snippet,contentDetails")

    q1 = base_channel_url%(youtube_channel_external_key,yt_api_key)
    r1 = requests.get(q1)
    j1 = json.loads(r1.text)

    ## This produces a playlist ID that includes all uploads for that channel ID
    upload_playlist_id = j1['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    nextPageToken = ''
    maxResults = 5    

    more_videos_on_channel = True

    ## WHILE loop - are there new videos on this channel?
    while more_videos_on_channel:
        discovered_datetime = datetime.now(timezone.utc)

        ## Use API to pull the most recent five videos
        base_url_n = ("https://www.googleapis.com/youtube/v3/playlistItems"
            "?playlistId=%s"
            "&key=%s"
            "&part=snippet"
            "&pageToken=%s"
            "&maxResults=%s")

        qn = base_url_n%(upload_playlist_id,yt_api_key,nextPageToken,maxResults)
        rn = requests.get(qn)
        jn = json.loads(rn.text)        

        if 'nextPageToken' in jn.keys():
            nextPageToken = jn['nextPageToken']
        else:
            more_videos_on_channel = False

        ## youtube_channel_id defined above
        video_type_id = 1 # To be modified later
        stats_tracking = False # To be modified later

        published_datetimes = unpack_video_discovery_json(jn,'publishedAt')
        video_titles = unpack_video_json(jn,'title')
        video_descriptions = unpack_video_json(jn,'description')
        video_thumbnail_urls = unpack_video_json(jn,'thumbnails','high','url')
        youtube_video_external_keys = unpack_video_json(jn,'resourceId','videoId')

        # Necessary to get video length and some other options
        composite_external_key = ",".join(youtube_video_external_keys)
        nkeys = len(youtube_video_external_keys)
        base_url = ("https://www.googleapis.com/youtube/v3/videos"
                "?id=%s"
                "&key=%s"
                "&part=contentDetails")

        qn = base_url%(composite_external_key,yt_api_key)
        rn = requests.get(qn)
        jn = json.loads(rn.text)

        video_durations = unpack_video_json(jn,'duration',part="contentDetails")
        video_captions = unpack_video_json(jn,'caption',part="contentDetails")
        video_licensed = unpack_video_json(jn,'licensedContent',part="contentDetails")

        insert_query = ('INSERT INTO "YouTube_Videos" '
                '(youtube_channel_id,video_type_id,published_datetime,discovered_datetime,'
                'video_title,video_description,youtube_video_external_key,video_duration,'
                'video_thumbnail_url,stats_tracking,video_captions,video_licensed) '
                'values %s')

        ## FOR loop over those videos
        data = []
        for i in range(nkeys):
            external_key = youtube_video_external_keys[i]

            ## IF a video is not already in the DB, add it
            if external_key in prev_external_keys:
                more_videos_on_channel = False
            else:
                prev_external_keys.append(external_key)
                row = (channel_id[0], # Because we made this a tuple earlier
                    video_type_id,
                    published_datetimes[i],
                    discovered_datetime,
                    video_titles[i],
                    video_descriptions[i],
                    youtube_video_external_keys[i],
                    video_durations[i],
                    video_thumbnail_urls[i],
                    stats_tracking,
                    video_captions[i],
                    video_licensed[i]
                    )
                data.append(row)

        execute_values(
            cur, insert_query, data
        )
        conn.commit()

cur.close()
conn.close()

script_end_time = datetime.now()

path_inc_script = argv[0]
temp_str = path_inc_script.split('/')
temp_str[-1] = ''
path_to_script = '/'.join(temp_str)

timing_output_file = open(path_to_script+"timing.txt","a")
print(script_end_time-script_start_time,file=timing_output_file)
timing_output_file.close()

