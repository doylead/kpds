import json
from isodate import parse_duration
from datetime import datetime, timezone
import psycopg2
from psycopg2 import sql
from os import environ

yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

def table_exists(table_name,schema_name="YouTube_Video_Stats"):
    ## Checks the database to see if a table with a provided name
    ## exists.  If it does, return True.
    # Works as intended
    query = sql.SQL("select * from pg_tables where schemaname=%s and tablename=%s")
    cur.execute(query,[schema_name,table_name])
    results = cur.fetchall()
    exists = (len(results)==1)
    return exists


def create_video_stats_table(table_name):
    ## Creates a table to store time series data for YouTube video
    # Works as intended
    query_string = ("CREATE TABLE {schema_table} "
        "(scan_datetime TIMESTAMPTZ, "
        "view_count BIGINT, "
        "like_count INTEGER, "
        "dislike_count INTEGER, "
        "comment_count INTEGER, "
        "favorite_count INTEGER)")
    query = sql.SQL(query_string).format(
        schema_table = sql.Identifier("YouTube_Video_Stats",table_name)
        )
    cur.execute(query)
    conn.commit()

def add_video_stats_data(table_name,data):
    ## Adds a row of data to a YouTube_Video_Stats table
    # WIP
    # May be an area for future security improvement?
    query_string = ("INSERT INTO {shema_table} "
        "(scan_datetime, view_count, like_count, dislike_count, "
        "comment count, favorite count) VALUES "
        "(%s, %s, %s, %s, %s, %s)")
    query = sql.SQL(query_string).format(
        schema_table = sql.Identifier("YouTube_Video_Stats",table_name)
        )
    cur.execute(query,data)

