from fastapi import FastAPI
import datetime as dt
from read_db import ReadDB
from pydantic import BaseModel
from utils.models import Input

app = FastAPI()
readdb = ReadDB()

@app.get("/")
async def root():
	return {"message": "Hello World"}

@app.post("/retrieve_data")
async def retrieve_data(input: Input):
	print("starting db reading")
	output = readdb.get_rawdata(tagname=input.var, start_ux=input.start, end_ux = input.end)

	return output['data'].to_json()

@app.post('/recieve_output')
async def receive_output(df_in: str):
	df = pd.DataFrame.read_json(df_in)
	return df
