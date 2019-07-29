import requests
import json
from os import environ

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

channel_id = 'UCp-pqXsizklX3ZHvLxXyhxw'
yt_api_key = environ['YT_API_KEY']

base_url_1 = ("https://www.googleapis.com/youtube/v3/channels"
	"?id=%s"
	"&key=%s"
	"&part=contentDetails")

q1 = base_url_1%(channel_id,yt_api_key)
r1 = requests.get(q1)
j1 = json.loads(r1.text)

## This produces a playlist ID that includes all uploads for that channel ID
upload_playlist_id = j1['items'][0]['contentDetails']['relatedPlaylists']['uploads']


## Archives the title of each video
video_titles = []
nextPageToken = '' # The first pageToken we pass is empty - the first page in the playlist
morePages = True # The loop control variable - are there any more pages?

while morePages:
	base_url_n = ("https://www.googleapis.com/youtube/v3/playlistItems"
        	"?playlistId=%s"
        	"&key=%s"
        	"&part=snippet"
		"&pageToken=%s"
        	"&maxResults=3")

	qn = base_url_n%(upload_playlist_id,yt_api_key,nextPageToken)
	rn = requests.get(qn)
	jn = json.loads(rn.text)

	if 'nextPageToken' in jn.keys():
		nextPageToken = jn['nextPageToken']
	else:
		morePages = False

	nvideos = len(jn['items'])
 	for i in range(0,nvideos):
		this_title = jn['items'][i]['snippet']['title']
		video_titles.append(this_title)


print video_titles[-1]


