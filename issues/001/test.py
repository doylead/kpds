import psycopg2
from psycopg2.extras import execute_values
import codecs
import requests
import json
from os import environ
from datetime import datetime, timezone, timedelta
from isodate import parse_duration

yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

# Get time from SQL database
video_query = 'SELECT published_datetime,youtube_video_external_key FROM "YouTube_Videos" LIMIT 100;'
cur.execute(video_query)
video_results = cur.fetchall()
sql_time = video_results[0][0]

cur.close()
conn.close()


# Get DateTime Python
python_time = datetime.now(timezone.utc)
# To test comparison logic, we get a value from the far past (~10 years ago)
python_shifted_time = python_time - timedelta(days=3650)


# JSON from YouTube API
external_key = video_results[5][1]
base_url = ("https://www.googleapis.com/youtube/v3/videos"
        "?id=%s"
        "&key=%s"
        "&part=snippet")

qn = base_url%(external_key,yt_api_key)
rn = requests.get(qn)
jn = json.loads(rn.text)

api_time_preformat = jn['items'][0]['snippet']['publishedAt']
api_time = datetime.strptime(api_time_preformat, '%Y-%m-%dT%H:%M:%S.%fZ')
api_time = api_time.astimezone(timezone.utc)

# Comparisons
print('Note: SQL time comes from one video, API time from an older video, an Python times from now()')
print('')

print('External Key: %s'%external_key)
print('SQL Time: %s'%sql_time)
print('Now (DateTime): %s'%python_time)
print('API Time: %s'%api_time)
print('')

print('Is shifted python time before SQL time?')
print(python_shifted_time<sql_time)
print('')

print('Is python time before SQL time?')
print(python_time<sql_time)
print('')

print('Is API time before SQL time?')
print(api_time<sql_time)
print('')

