<h2>Description of columns used in table YouTube_Videos</h2>

**youtube_video_id** (serial) - A numerical index for YouTube Videos.  Primary key for this table

**youtube_channel_id** (integer) - A numerical index for YouTube channels.  Foreign key for the YouTube_Channels table

**video_type_id** (integer) - A numerical index for video types.  Foreign key for the Video_Types table

**published_datetime** (timestamp w/tz) - The time the video was published to YouTube

**discovered_datetime** (timestamp w/tz) - The time the video was first found by our crawlers

**video_title** (varchar) - TEXT

**video_description** (varchar) - The video’s description on YouTube at the time of discovery

**youtube_video_external_key** (varchar(11)) - The identifying URL fragment from YouTube.  YouTube ensures it is unique

**video_duration** (integer) - The video’s run length, measured in seconds

**video_thumbnail_url** (varchar) - TEXT

**stats_tracking** (boolean) - Whether time series data is being recorded for this video (1/True indicates data is being logged)

**stats_frequency** (integer) - TEXT

**video_captions** (boolean) - TEXT

**video_licensed** (boolean) - TEXT
