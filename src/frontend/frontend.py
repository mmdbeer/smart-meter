import streamlit as st
import pandas as pd
import numpy as np
import requests
import datetime as dt
import json
import time
import matplotlib.pyplot as plt
import plotly.express as px

class Frontend():
	def __init__(self):
		st.set_page_config(page_title="The amazing smartmeter app",
				layout="wide",
				page_icon = "src/frontend/favicon.ico"
				)
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

	def parse_json_to_df(self,jsfile,var):

		data = json.loads(jsfile)

		dates = []
		vallist = []

		for key in data[var]:
			try:
				val = float(data[var][key])
			except:
				val = float('nan')
			date = dt.datetime.fromtimestamp(float(key))
			dates.append(str(date))
			vallist.append(val)
		df = pd.DataFrame(index=dates,data=vallist,columns=[var])
		df.index = pd.to_datetime(df.index)

		return df

	def set_fig_fontsize(self,ax,fontsize):
		for item in ([ax.title, ax.axis.label, ax.yaxis.label] + ax.get_xticklabels()+ax.get_yticklabels()):
			item.set_fontsize(fontsize)

	def startup_frontend(self):
		st.title("The amazing smartmeter app")
		col1,col2 = st.columns(2)

		with col1:
			start = st.date_input("Startdate", dt.date.today()-dt.timedelta(1))
			end =  st.date_input("Enddate", dt.date.today()+dt.timedelta(1))
		with col2:
			time_val = st.number_input('time interval for binning',min_value=1,value=5)
			time_unit = st.selectbox('select time unit', ('m','h','d','w','y'),index=0)

		data = {}
		df = pd.DataFrame()

		for var in  ['gas','elec_t1','elec_t2','elec_-t1','elec_-t2']:
			input = {'start': time.mktime(start.timetuple()),
				'end': time.mktime(end.timetuple()),
				'var': var,
				'time_val':time_val,
				'time_unit':time_unit,
				}

			res = self.send_to_server('/retrieve_data',input)
			#st.write(res.status_code)
			if res.status_code == 200:
				data[var] = self.parse_json_to_df(res.json(),var)
				if df.empty:
					df = data[var].copy()
				else:
					df = pd.concat([df,data[var]],axis=1)
		df['date'] = df.index
		#df=df.rename(columns={'elec_t1':'low','elec_t2':'high'})
		df['drawn']=df['elec_t1']+df['elec_t2']
		df['delivered']=df['elec_-t1']+df['elec_-t2']

		col3,col4 = st.columns(2)
		with col3:
			st.subheader("Gas usage")
			fig_g = px.line(df,x='date',y='gas',
					labels={'date': '',
						'gas': 'Gas used [m3]'
						}
					)

			st.plotly_chart(fig_g)
			#fig, ax = plt.subplots(figsize=(20,10))
			#ax.plot(data['gas'].index,data['gas']['gas'],label='gas')
			#ax.legend()
			#ax.set(xlabel='date')
			#fontsize=20
			#ax.xaxis.label.set_fontsize(fontsize)
			#ax.yaxis.label.set_fontsize(fontsize)
			#for tick in ax.xaxis.get_major_ticks():
			#	tick.label.set_fontsize(fontsize)
			#for tick in ax.yaxis.get_major_ticks():
		#		tick.label.set_fontsize(fontsize)
		#	st.pyplot(fig)

		with col4:
			st.subheader("Electricity")
			fig_e=px.line(df,x='date',y=['drawn','delivered'],
					labels={'date':'',
						'value':'Electricity [kWh]',
						'variable':'Direction'
						}
					)
			st.plotly_chart(fig_e)
			#fig, ax = plt.subplots(figsize=(20,10))
			#ax.plot(data['elec_t1'].index,data['elec_t1']['elec_t1'],label='elec_t1')
			#ax.plot(data['elec_t2'].index,data['elec_t2']['elec_t2'],label='elec_t2')
			#ax.legend()
			#ax.set(xlabel='date')
			#fontsize=20
			#ax.xaxis.label.set_fontsize(fontsize)
			#ax.yaxis.label.set_fontsize(fontsize)
			#for tick in ax.xaxis.get_major_ticks():
			#	tick.label.set_fontsize(fontsize)
			#for tick in ax.yaxis.get_major_ticks():
			#	tick.label.set_fontsize(fontsize)
			#st.pyplot(fig)

if __name__ == '__main__':
	frontend = Frontend()
	frontend.startup_frontend()
