import os
import sqlite3 as sq
from sqlite3 import Error
import datetime as dt
import yaml
import time

def create_connection(path):
	connection = None
	try:
		connection = sq.connect(path)
		print("successful connection to db")
	except Error as e:
		print(f"db connection failed, error {e}")

	return connection

def execute_read_query(connection, query):
	cursor = connection.cursor()
	result = None
	try:
		cursor.execute(query)
		result = cursor.fetchall()
		return result
	except Error as e:
		print(f"Error reading data: {e}")

def datetime_to_unix(timestamp_dt):
	unix = time.mktime(timestamp_dt.timetuple())
	return unix

def get_rawdata(tagname,start_dt,end_dt):

	start_ux = datetime_to_unix(start_dt)
	end_ux = datetime_to_unix(end_dt)

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
	data = execute_read_query(connection,select_data)

	return data

if __name__ == "__main__":

	cwd = os.getcwd()
	rootkey = 'smartmeter'
	root = os.path.join(cwd.split(rootkey)[0],rootkey)

	with open(os.path.join(root,'config','config.yml'),'r') as f:
		conf = yaml.safe_load(f)

	db = conf['database']['name']
	connection = create_connection(os.path.join(root,conf['dirs']['database'],db))

	tag = 'elec_t2'
	start_dt = dt.datetime(2022,1,1,0,0,0)
	end_dt = dt.datetime.now()

	data = get_rawdata(tag,start_dt,end_dt)
	print(data)
