CREATE TABLE "YouTube_Videos" (
 youtube_video_id BIGSERIAL,
 youtube_channel_id INTEGER,
 video_type_id INTEGER,
 published_datetime TIMESTAMP WITH TIME ZONE,
 discovered_datetime TIMESTAMP WITH TIME ZONE,
 video_title VARCHAR,
 video_description VARCHAR,
 youtube_video_external_key VARCHAR(11),
 video_duration INTEGER,
 video_thumbnail_url VARCHAR,
 tracking BOOLEAN DEFAULT 'false',
 scan_frequency INTEGER,
 video_captions BOOLEAN,
 video_licensed BOOLEAN
);

ALTER TABLE "YouTube_Videos" ADD CONSTRAINT YouTube_Videos_pkey PRIMARY KEY (youtube_video_id);

CREATE TABLE "YouTube_Channels" (
 youtube_channel_id BIGSERIAL,
 published_datetime TIMESTAMP WITH TIME ZONE,
 discovered_datetime TIME WITH TIME ZONE,
 channel_title VARCHAR,
 channel_description VARCHAR,
 channel_custom_url VARCHAR,
 youtube_channel_external_key VARCHAR,
 tracking BOOLEAN DEFAULT 'false',
 scan_frequency INTEGER,
 initial_scan BOOLEAN DEFAULT 'false'
);

ALTER TABLE "YouTube_Channels" ADD CONSTRAINT YouTube_Channels_pkey PRIMARY KEY (youtube_channel_id);

CREATE TABLE "Video_Types" (
 video_type_id BIGSERIAL,
 type_name VARCHAR(25)
);

ALTER TABLE "Video_Types" ADD CONSTRAINT Video_Types_pkey PRIMARY KEY (video_type_id);

ALTER TABLE "YouTube_Videos" ADD CONSTRAINT YouTube_Videos_youtube_channel_id_fkey FOREIGN KEY (youtube_channel_id) REFERENCES "YouTube_Channels"(youtube_channel_id);
ALTER TABLE "YouTube_Videos" ADD CONSTRAINT YouTube_Videos_video_type_id_fkey FOREIGN KEY (video_type_id) REFERENCES "Video_Types"(video_type_id);

INSERT INTO "Video_Types"(type_name) VALUES ('Uncategorized');
GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO world;
