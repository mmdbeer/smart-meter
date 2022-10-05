import os
import sqlite3 as sq
from sqlite3 import Error
import datetime as dt
import yaml
import time
import pandas as pd
import json

class ReadDB:

	def __init__(self):
		cwd = os.getcwd()
		rootkey = 'utilities'
		root = os.path.join(cwd.split(rootkey)[0],rootkey)

		with open(os.path.join(root,'config','config.yml'),'r') as f:
			conf = yaml.safe_load(f)

		db = conf['database']['name']
		self.connection = self.create_connection(os.path.join(root,conf['dirs']['database'],db))
		self.server_url = "http://0.0.0.0:8432"

	def create_connection(self,path):
		connection = None
		try:
			connection = sq.connect(path)
			print("successful connection to db")
		except Error as e:
			print(f"db connection failed, error {e}")

		return connection

	def execute_read_query(self, query):
		cursor = self.connection.cursor()
		result = None
		try:
			cursor.execute(query)
			result = cursor.fetchall()
			return result
		except Error as e:
			print(f"Error reading data: {e}")

	def datetime_to_unix(self,timestamp_dt):
		unix = time.mktime(timestamp_dt.timetuple())
		return unix

	def get_rawdata(self,tagname,start_ux,end_ux):

		select_data = """
		SELECT
			rawdata.timestamp,
			rawdata.value
		FROM
			rawdata
		WHERE
			rawdata.tag_name = '""" + str(tagname) + """'
		AND
			rawdata.timestamp BETWEEN """ + str(start_ux) + """ and """ + str(end_ux) + """;
		"""
		data = self.execute_read_query(select_data)

		dt_list=[]
		data_list=[]
		for tuple in data:
			dt_list.append(tuple[0])
			data_list.append(float(tuple[1])) 

		df = pd.DataFrame(data=data_list,index=dt_list,columns=[tagname])

		self.send_output_to_server(df)
		return {'data':df}

	def send_output_to_server(self,data):
		url =self.server_url + r'/recieve_output'
		timestamp = time.time()
		output = {"data":data.to_json()}
		try:
			req = requests.post(url,data)
		except:
			pass

if __name__ == "__main__":

	tag = 'gas'
	start_dt = dt.datetime(2022,1,1,0,0,0)
	end_dt = dt.datetime.now()
	read_db = ReadDB()
	data = read_db.get_rawdata(tag,read_db.datetime_to_unix(start_dt),read_db.datetime_to_unix(end_dt))
	print(data)
