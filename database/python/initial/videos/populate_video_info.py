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

channel_query = 'SELECT youtube_channel_id,youtube_channel_external_key FROM "YouTube_Channels" ORDER BY youtube_channel_id;'
cur.execute(channel_query)
channel_results = cur.fetchall()
#channel_results = channel_results[:5]

for result in channel_results:
    (youtube_channel_id,youtube_channel_external_key) = result

    base_url_1 = ("https://www.googleapis.com/youtube/v3/channels"
                "?id=%s"
                "&key=%s"
                "&part=snippet,contentDetails")

    q1 = base_url_1%(youtube_channel_external_key,yt_api_key)
    r1 = requests.get(q1)
    j1 = json.loads(r1.text)

    ## This produces a playlist ID that includes all uploads for that channel ID
    upload_playlist_id = j1['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    nextPageToken = ''
    morePages = True # The loop control variable - are there any more pages?

    while morePages:
        base_url_n = ("https://www.googleapis.com/youtube/v3/playlistItems"
            "?playlistId=%s"
            "&key=%s"
            "&part=snippet"
            "&pageToken=%s"
            "&maxResults=50")

        qn = base_url_n%(upload_playlist_id,yt_api_key,nextPageToken)
        rn = requests.get(qn)
        jn = json.loads(rn.text)
        
        for ji in jn['items']: # Loop over the videos
            # youtube_channel_id defined above
            video_type_id = 1 # Uncategorized
            published_datetime = ji['snippet']['publishedAt']
            discovered_datetime = datetime.now(timezone.utc)
            video_title = ji['snippet']['title']
            video_description = ji['snippet']['description']
            youtube_video_external_key = ji['snippet']['resourceId']['videoId']
            video_length = 0 # Not accessible in these API calls
            video_thumbnail_url = ji['snippet']['thumbnails']['high']['url']
            tracking = False # Do not track by default

            insertstring = ('INSERT INTO "YouTube_Videos" '
                '(youtube_channel_id,video_type_id,published_datetime,discovered_datetime,video_title,video_description,youtube_video_external_key,video_length,video_thumbnail_url,tracking) '
                'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
            line_list = (youtube_channel_id,video_type_id,published_datetime,discovered_datetime,video_title,video_description,youtube_video_external_key,video_length,video_thumbnail_url,tracking)
            cur.execute(insertstring,line_list)

        if 'nextPageToken' in jn.keys():
            nextPageToken = jn['nextPageToken']
        else:
            morePages = False 

conn.commit()
cur.close()
conn.close()
