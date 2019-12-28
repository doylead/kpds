import psycopg2
from psycopg2.extras import execute_values
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone
from isodate import parse_duration

def unpack_video_json(json_object,cat1,cat2=None,cat3=None,part='snippet'):
    maxResults = len(json_object['items'])

    # Extract information
    if cat3 is not None:
        l = [json_object['items'][i][part][cat1][cat2][cat3] for i in range(maxResults)]
    elif cat2 is not None:
        l = [json_object['items'][i][part][cat1][cat2] for i in range(maxResults)]
    else:
        l = [json_object['items'][i][part][cat1] for i in range(maxResults)]

    # Process if necessary
    # Convert duration to seconds
    if cat1 == 'duration':
        l = [int(parse_duration(l[i]).total_seconds()) for i in range(maxResults)]

    # Format Boolean variables
    if cat1 == 'caption':
        l = [json.loads(l[i]) for i in range(maxResults)]

    # Converts timezone to UTC
    if cat1 == 'publishedAt':
        l = [datetime.strptime(l[i], "%Y-%m-%dT%H:%M:%S.%fZ") for i in range(maxResults)]
        l = [l[i].astimezone(timezone.utc) for i in range(maxResults)]

    return l

## Define important environmental variables
## Working as intended
yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

## Bring up the list of all channels we know about, assume a full crawling on all of them (should I adjust this?)
## Working as intended
channel_query = 'SELECT youtube_channel_id,youtube_channel_external_key FROM "YouTube_Channels" ORDER BY youtube_channel_id;'
cur.execute(channel_query)
channel_results = cur.fetchall()
channel_results = channel_results[66:] # for testing


## Going through each channel
## Working as intended
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
    maxResults = 50

    while morePages:
        discovered_datetime = datetime.now(timezone.utc)

        # This will not provide all desired information, e.g. video length
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
            morePages = False

        ## youtube_channel_id defined above
        video_type_id = 1 # To be modified later
        tracking = False # To be modified later

        published_datetimes = unpack_video_json(jn,'publishedAt')
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
                'video_thumbnail_url,tracking,video_captions,video_licensed) '
                'values %s')

        data = []
        for i in range(nkeys):
            row = (youtube_channel_id,
                video_type_id,
                published_datetimes[i],
                discovered_datetime,
                video_titles[i],
                video_descriptions[i],
                youtube_video_external_keys[i],
                video_durations[i],
                video_thumbnail_urls[i],
                tracking,
                video_captions[i],
                video_licensed[i]
            )
            data.append(row)

        # Allows us to add all 50 rows at once
        execute_values(
            cur, insert_query, data
        )
        conn.commit()

cur.close()
conn.close()
