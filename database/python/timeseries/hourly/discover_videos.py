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

### Pseudocode in-line for easier development

## Query DB for channels actively being tracked at this frequency

## Declare necessary logic variables

## Outer FOR loop through channels

    ## Query DB for videos on this channel

    ## WHILE loop - are there new videos on this channel?

        ## Use API to pull the most recent five videos

        ## FOR loop over those videos

            ## IF a video is not already in the DB, add it

            ## ELSE condition for WHILE loop is false



