import psycopg2
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone
from isodate import parse_duration


yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

video_query = 'SELECT youtube_video_external_key FROM "YouTube_Videos" WHERE video_length=0;'
cur.execute(video_query)
video_results = cur.fetchall()
video_results = video_results[:5000]

num_video_keys = len(video_results)
max_batch_size = 50
split_external_keys = []

for i in range((num_video_keys+max_batch_size-1)//max_batch_size):
    start_index = i*max_batch_size
    end_index = (i+1)*max_batch_size
    key_chunk = video_results[start_index:end_index]
    flat_key_chunk = [item for sublist in key_chunk for item in sublist]
    split_external_keys.append(flat_key_chunk)

request_keys = []

for key_chunk in split_external_keys:
    composite_key = ",".join(key_chunk)
    request_keys.append( composite_key )

num_requests = len(request_keys)

for i in range(num_requests):
    composite_key = request_keys[i]

    base_url = ("https://www.googleapis.com/youtube/v3/videos"
            "?id=%s"
            "&key=%s"
            "&part=contentDetails")

    q = base_url%(composite_key,yt_api_key)
    r = requests.get(q)
    j = json.loads(r.text)

    for video_response in j['items']:
        duration = video_response['contentDetails']['duration']
        duration_seconds = int(parse_duration(duration).total_seconds())
        external_key = video_response['id']
        updatestring = ('UPDATE "YouTube_Videos" '
                'SET video_length = %s '
                'WHERE youtube_video_external_key = %s')
        line_list = (duration_seconds,external_key)
        cur.execute(updatestring,line_list)

conn.commit()
cur.close()
conn.close()

print("\a")
