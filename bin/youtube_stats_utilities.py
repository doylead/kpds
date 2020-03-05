import json
from isodate import parse_duration
from datetime import datetime, timezone



def table_exists(self,tabname):
    ## Checks the database to see if a table with a provided name
    ## exists.  If it does, return True.
    ## WIP

    query = "SELECT * FROM pg_tables WHERE tablename='youtube_video_stats.%s'"%tabname
    self.cursor.execute(query)
    results = self.cursor.fetchall()
    return len(results)==1

def create_table(self,tabname):
    ## Creates a table to store time series data for YouTube video
    ## WIP

    create_command = ' '.join((
        'CREATE TABLE "youtube_video_stats.%s"'%tabname,
        '(scan_datetime TIMESTAMP WITH TIMEZONE,',
        'view_count BIGINT,',
        'like_count INTEGER,',
        'dislike_count INTEGER,',
        'comment_count INTEGER,',
        'favorite_count INTEGER)'
        ))
    self.cursor.execute(create_command)


