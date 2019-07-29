import os.path
from os import environ
import requests
import psycopg2
import pickle
import json
from datetime import datetime

class YouTube_Video_DB(object):

	def __init__(self):
		# Opens a connection to pull static data
		connstring = "dbname='kpds' host='localhost'"
		connstring += "user='%s'"%environ['DBUSER']
		connstring += "password='%s'"%environ['DBPASS']
		conn = psycopg2.connect(connstring)
		cursor = conn.cursor()
		
		cursor.execute("SELECT link FROM youtubesummary")
		results = cursor.fetchall()
		raw_url_list = [item for sublist in results for item in sublist]
		self.yt_keys = [raw_url.split('=')[1] for raw_url in raw_url_list]
		self.yt_api_key = environ['YT_API_KEY']
		conn.close()

		# Opens a connection for adding time series data
		self.connstring = "dbname='youtubetimeseries' host='localhost'"
		self.connstring += "user='%s'"%environ['DBUSER']
		self.connstring += "password='%s'"%environ['DBPASS']
		self.conn = psycopg2.connect(self.connstring)
		self.cursor = self.conn.cursor()
		

	def create_table(self,tabname):
		create_command = ' '.join((
				'CREATE TABLE "%s"'%tabname, 
				'(timeStamp varchar,', 
				'viewCount numeric,', 
				'likeCount numeric,', 
				'dislikeCount numeric,', 
				'commentCount numeric)'
				))
		self.cursor.execute(create_command)
		
	def table_exists(self,tabname):
		query = "SELECT * FROM pg_tables WHERE tablename='%s'"%tabname
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		return len(results)==1

	def log(self):
		m = 50 # max query size
		# Next line splits self.yt_keys into sublists of at most m keys
		split_keys = [self.yt_keys[i*m:(i+1)*m] for i in range((len(self.yt_keys)+m-1)//m)]

		# Get the current time in UTC
                dt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

		all_items = []
		for section in split_keys:
			mega_key = ",".join(section)
			base_url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id=%s&key=%s'
			query_url = base_url%(mega_key, self.yt_api_key)
			r = requests.get(query_url)
			parsed_json = json.loads(r.text)
			#diag = open('/home/doylead/kpds/scraping/scripts/diag.pickle','w')
			#pickle.dump(parsed_json,diag)
			#diag.close()
			all_items += parsed_json['items']

		# At this point all_items contains a list of all data,
		# we just need to get it to SQL
		for item in all_items:
			stats = item['statistics']
			if 'viewCount' not in stats.keys():
				stats['viewCount']=0
			if 'likeCount' not in stats.keys():
				stats['likeCount']=0
			if 'dislikeCount' not in stats.keys():
				stats['dislikeCount']=0
			if 'commentCount' not in stats.keys():
				stats['commentCount']=0

			tabname = item['id']

			row = [
				dt,
				int(stats['viewCount']),
				int(stats['likeCount']),
				int(stats['dislikeCount']),
				int(stats['commentCount']),
			]

			if not self.table_exists(tabname):
				self.create_table(tabname)
		
			insert_command = ' '.join([
				'INSERT INTO "%s"'%tabname,
				'(timestamp,',
				'viewCount,',
				'likeCount,',
				'dislikeCount,',
				'commentCount)',
				'VALUES (%s,%s,%s,%s,%s)',
				])
			self.cursor.execute(insert_command,row)
			self.conn.commit()

