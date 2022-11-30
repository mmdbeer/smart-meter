import os
import sqlite3 as sq
from sqlite3 import Error
import datetime as dt
import yaml
import time
import pandas as pd
import json
import numpy as np

class ReadDB:

	def __init__(self):
		cwd = os.getcwd()
		rootkey = 'smart-meter'
		self.root = os.path.join(cwd.split(rootkey)[0],rootkey)

		with open(os.path.join(self.root,'config','config.yml'),'r') as f:
			conf = yaml.safe_load(f)

		self.db = conf['database']['name']
		self.db_dir = conf['dirs']['database']

		self.server_url = "http://0.0.0.0:8432"

		self.time_units = {'m':60,'h':3600,'d':24*3600,'w':7*24*3600,'y':365*24*3600}

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

	def find_nearest(self,array,value):
		array = np.asarray(array)
		idx = (np.abs(array-value)).argmin()
		return idx

	def get_data(self,tagname,start_ux,end_ux,bin: tuple = None):

		self.connection = self.create_connection(os.path.join(self.root,self.db_dir,self.db))

		df = self.get_rawdata(tagname,start_ux,end_ux)['data']
		df = df.sort_index(ascending=True)

		if bin:
			if not bin[1] in self.time_units:
				print('Warning, wrong binning input! Showing raw data instead')
			else:
				tstep = bin[0]*self.time_units[bin[1]]
			idx0 = len(df)-1
			t0 = df.index[idx0]
			tend = df.index[0]
			t = t0
			tlist=[]
			vallist=[]
			while t-tstep>tend:
				idx1 = self.find_nearest(df.index,t-tstep)
				t1 = df.index[idx1]
				if t1 == t:
					if idx1>0:
						t1 = df.index[idx1-1]
					else:
						break
				val = df.loc[t,tagname]-df.loc[t1,tagname]
				tlist.append(float(t))
				try:
					vallist.append(float(val))
				except:
					vallist.append(float('nan'))

				t = t1

			dfbin = pd.DataFrame(data=vallist,index=tlist,columns=[tagname])
			sumcheck =abs(dfbin.sum(axis=0)[tagname]-(df.loc[df.index[-1],tagname]-df.loc[t,tagname]))/dfbin.sum(axis=0)[tagname]
			print(sumcheck)
			if sumcheck > 0.05:
				print('ERROR: data binning not correct')
				#raise Exception('data binning not correct')
		else:
			self.connection.close()
			return {'data':df}

		self.connection.close()
		return {'data':dfbin}

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
			try:
				data_list.append(float(tuple[1]))
			except:
				data_list.append(float('nan'))

		df = pd.DataFrame(data=data_list,index=dt_list,columns=[tagname])

		#self.send_output_to_server(df)
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

	read_db = ReadDB()
	start = read_db.datetime_to_unix(dt.datetime(2022,1,1,0,0,0))
	end_dt = read_db.datetime_to_unix(dt.datetime.now())
	bin=(1,'h')
	data = read_db.get_data(tag,start,end_dt,bin)
	print(data['data'])
