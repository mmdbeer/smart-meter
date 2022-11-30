import sqlite3 as sq
import os
import yaml

def create_connection(path):
	connection = None
	try:
		connection = sq.connect(path)
		print("Connection to SQLite db successfull")
	except Error as e:
		print(f"Failed to connect to db, error: {e}")

	return connection

def execute_query(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
	except Error as e:
		print(f"Error: {e}")
		print(f"Query: {query}")

def create_data_table(table,connection,cols,prim_key):

	create_table_str = """
	CREATE TABLE IF NOT EXISTS """ + str(table) + """ ( """

	for col in cols:
		for key in col:
			create_table_str +=  key + " " + col[key] + ", "

	create_table_str += "PRIMARY KEY " + str(prim_key)
	create_table_str += ");"

	execute_query(connection, create_table_str)

if __name__ == "__main__":

	cwd = os.getcwd()
	rootkey = 'smart-meter'
	root = os.path.join(cwd.split(rootkey)[0],rootkey)

	with open(os.path.join(root,'config','config.yml'),"r") as f:
		conf = yaml.safe_load(f)

	db = conf['database']['name']

	connection = create_connection(os.path.join(root,conf['dirs']['database'],db))
	for table in conf['database']['tables']:
		create_data_table(table=table,connection=connection,cols=conf['database']['tables'][table]['cols'],prim_key=conf['database']['tables'][table]['primary key'])
	connection.close()
