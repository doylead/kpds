<h2>Description of columns used in table YouTube_Videos</h2>

**youtube_video_id** (serial) - A numerical index for YouTube Videos.  Primary key for this table

**youtube_channel_id** (integer) - A numerical index for YouTube channels.  Foreign key for the YouTube_Channels table

**video_type_id** (integer) - A numerical index for video types.  Foreign key for the Video_Types table

**published_datetime** (timestamp w/tz) - The time the video was published to YouTube

**discovered_datetime** (timestamp w/tz) - The time the video was first found by our crawlers

**video_title** (varchar) - The video's title on YouTube at the time of discovery

**video_description** (varchar) - The video’s description on YouTube at the time of discovery

**youtube_video_external_key** (varchar(11)) - The identifying URL fragment from YouTube.  YouTube ensures it is unique

**video_duration** (integer) - The video’s run length, measured in seconds

**video_thumbnail_url** (varchar) - A URL pointing to the video thumbnail

**stats_tracking** (boolean) - Whether time series data is being recorded for this video (True indicates data is being collected)

**stats_frequency** (integer) - The time between sequential statistics calls, measured in minutes

**video_captions** (boolean) - Whether or not this video has captions (True indicates video is captioned)

**video_licensed** (boolean) - Whether or not this video has licensed content (True indicates video is licensed)
