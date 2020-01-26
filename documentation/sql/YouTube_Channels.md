<h2>Description of columns used in table YouTube_Channels</h2>

**youtube_channel_id** (serial) – A numerical index for YouTube Channels.  Primary key for this table

**published_datetime** (timestamp w/tz) – The time a channel was published to YouTube

**channel_title** (varchar) – The title of a channel at the time of discovery

**youtube_channel_external_key** (varchar(24)) – The identifying URL fragment from YouTube.  YouTube ensures it is unique

