import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime as dt
import json
import time
import matplotlib.pyplot as plt

class Frontend():
	def __init__(self):
		self.server_url = "http://0.0.0.0:8432"

	def send_to_server(self,path,data_dict:None):
		url = self.server_url
		url += path
		data = json.dumps(data_dict, indent = 4, sort_keys=True, default=str)
		if data_dict:
			req = requests.post(url,data=data)
		else:
			req = requests.get(url)
		return req

	def parse_json_to_df(self,jsfile):

		data = json.loads(jsfile)

		dates = []
		vallist = []

		for key in data[self.var]:
			val = float(data[self.var][key])
			date = dt.datetime.fromtimestamp(float(key))
			dates.append(str(date))
			vallist.append(val)
		df = pd.DataFrame(index=dates,data=vallist,columns=[self.var])
		df.index = pd.to_datetime(df.index)

		return df

	def set_fig_fontsize(self,ax,fontsize):
		for item in ([ax.title, ax.axis.label, ax.yaxis.label] + ax.get_xticklabels()+ax.get_yticklabels()):
			item.set_fontsize(fontsize)

	def startup_frontend(self):
		st.title('The amazing smartmeter app')

		start = st.date_input("Startdate", dt.date.today()-dt.timedelta(1))
		end =  st.date_input("Enddate", dt.date.today()+dt.timedelta(1))
		var = st.selectbox('select variable', ('gas','elec_t1','elec_t2','elec_-t1','elec_-t2'))
		time_val = st.number_input('time interval for binning',min_value=1,value=1)
		time_unit = st.selectbox('select time unit', ('m','h','d','w','y'),index=1)
		self.var = var
		if st.button('Retrieve data'):
			input = {'start': time.mktime(start.timetuple()),
				'end': time.mktime(end.timetuple()),
				'var': var,
				'time_val':time_val,
				'time_unit':time_unit,
				}
			res = self.send_to_server('/retrieve_data',input)

			data = self.parse_json_to_df(res.json())

			fig, ax = plt.subplots(figsize=(20,10))
			ax.plot(data.index,data[self.var],label=self.var)
			ax.legend()
			ax.set(xlabel='date')
			fontsize=20
			ax.xaxis.label.set_fontsize(fontsize)
			ax.yaxis.label.set_fontsize(fontsize)
			for tick in ax.xaxis.get_major_ticks():
				tick.label.set_fontsize(fontsize)
			for tick in ax.yaxis.get_major_ticks():
				tick.label.set_fontsize(fontsize)
#self.set_fig_fontsize(ax,16)
			st.pyplot(fig)

if __name__ == '__main__':
	frontend = Frontend()
	frontend.startup_frontend()
