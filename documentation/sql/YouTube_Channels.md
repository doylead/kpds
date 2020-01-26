<h2>Description of columns used in table YouTube_Channels</h2>

**youtube_channel_id** (serial) - A numerical index for YouTube Channels.  Primary key for this table

**published_datetime** (timestamp w/tz) - The time the channel was published to YouTube

**discovered_datetime** (timestamp w/tz) - The time the channel was first found by our crawlers

**channel_title** (varchar) - The channel's title at the time of discovery

**channel_description** (varchar) - The channel's description at the time of discovery

**channel_custom_url** (varchar) - The channel's custom URL (if applicable) at time of discovery

**youtube_channel_external_key** (varchar(24)) - The identifying URL fragment from YouTube.  YouTube ensures it is unique

**stats_tracking** (boolean) - Whether time series data is being recorded for this channel (True indicates data is being collected)

**stats_frequency** (integer) - The time between sequential statistics calls, in minutes

**initial_discovery** (boolean) - Whether an initial video gather has been performed for this channel (True indicates initial video discovery has taken place)

**discovery_tracking** (boolean) - Whether or not additional video discovery calls will be performed (True indicates discovery will continue)

**discovery_frequency** (integer) - The time between sequential discovery calls, in minutes

