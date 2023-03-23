import time
import datetime as dt
import argparse
import json
import sys
import serial
import re
import csv
import sqlite3 as sq
import os
import yaml
from sqlite3 import Error
import numpy as np

def open_serial_p1_port():
	ser = serial.Serial()
	ser.baudrate = 115200
	ser.bytesize = serial.SEVENBITS
	ser.parity = serial.PARITY_EVEN
	ser.stopbits = serial.STOPBITS_ONE
	ser.xonxoff = 0
	ser.rtscts = 0
	ser.timeout = 20
	ser.port = "/dev/ttyUSB0"

	try:
		ser.open()
	except:
		sys.exit("Error opening %s. Program stopped" % ser.name)

	return ser

def retrieve_p1_msg(ser):
	p1_counter = 0
	msg = []

	while p1_counter<32:
		p1_line = ''
		try:
			p1_raw = ser.readline()
		except:
			sys.exit("Serial port %s can't be read. Program stopped" % ser.name)
		p1_str = str(p1_raw)
		p1_line = p1_str.strip()
		msg.append(p1_line)
		p1_counter = p1_counter + 1

	return msg

def create_connection(path):
	connection = None
	try:
		connection = sq.connect(path)
		print("connection to db successful")
	except Error as e:
		print(f"Failed to connect to db, error: {e}")
	return connection

def insert_data(data,table,connection):
	connection.executemany('INSERT OR IGNORE INTO ' + table + ' (tag_name,timestamp,value) VALUES (?, ?, ?)',data)
	connection.commit()
	print("data succesfully inserted in db")

if __name__ == "__main__":

	cwd = os.getcwd()
	rootkey = "smart-meter"
	root = os.path.join(cwd.split(rootkey)[0],rootkey)

	with open(os.path.join(root,'config','config.yml'),"r") as f:
		conf = yaml.safe_load(f)

	db = conf['database']['name']
	vars = conf['vars']

	ser = open_serial_p1_port()

	ts = time.time()
	print(dt.datetime.now())

	msg = retrieve_p1_msg(ser)

	with open('latest_reading.txt',"w") as txtfile:
		for row in msg:
			txtfile.write("%s\n" % row)

	reading = {}
	datalist = []

	for var in vars:
		select_row = [row for row in msg if vars[var]['var_string'] in row]

		tmp = select_row[0].split(vars[var]['unit'])[0]
		val = tmp[tmp.rfind('(')+1:]
		try:
			val = float(val)
			print(f"{var}:{val}")
		except:
			print('Error no reading; non numerical value')
			val = np.nan

		datalist.append((var,ts,val))
		reading[var] = val

	connection = create_connection(os.path.join(root,conf['dirs']['database'],db))
	insert_data(datalist,"rawdata",connection)
	connection.close()

	try:
		ser.close()
	except:
		sys.exit("Failed to close %s. Program stopped" % ser.name)
