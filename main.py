import time
import datetime as dt
import argparse
import json
import sys
import serial
import re
import csv

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

p1_counter = 0
stack = []
ts = dt.datetime.now().strftime('%Y%m%d%H%M%S')

while p1_counter<72:
	p1_line = ''
	try:
		p1_raw = ser.readline()
	except:
		sys.exit("Serial port %s can't be read. Program stopped" % ser.name)
	p1_str = str(p1_raw)
	p1_line = p1_str.strip()
	stack.append(p1_line)
	p1_counter = p1_counter + 1


id = {	'gas_ts':{'regex':r'24.2.1',
		'loc':(13,26)},
	'gas':{	'regex':r'24.2.1',
		'loc':(28,37)},
	'elec_ts':{'regex':r'1.0.0',
		'loc':(12,25)},
	'elec_t1':{'regex':r'1.8.1',
		'loc':(12,22)},
	'elec_t2':{'regex':r'1.8.2',
		'loc':(12,22)},
	'elec_-t1':{'regex':r'2.8.1',
		'loc':(12,22)},
	'elec_-t2':{'regex':r'2.8.2',
		'loc':(12,22)}
	}

reading = {}

for variable in id:
	regex = re.compile(id[variable]['regex'])
	selected_row = list(filter(regex.search, stack))

	try:
		reading[variable] = float(selected_row[0][id[variable]['loc'][0]:id[variable]['loc'][1]])
	except:
		reading[variable] = selected_row[0][id[variable]['loc'][0]:id[variable]['loc'][1]]

with open("latest_reading.txt",'w') as fp:
	for line in stack:
		fp.write("%s\n" % line)

with open("latest_values.csv",'w') as csvfile:
	writer = csv.writer(csvfile)

	writer.writerow(('timestamp',ts))

	for unit in reading:
		writer.writerow((unit,reading[unit]))

try:
	ser.close()
except:
	sys.exit("Failed to close %s. Program stopped" % ser.name)


