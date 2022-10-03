import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title('The amazing smartmeter app')

server_url = "http://0.0.0.0:8432"
req = requests.get(server_url)
st.markdown(req.text)
