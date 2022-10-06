from pydantic import BaseModel

class Input(BaseModel):
	start: str
	end: str
	var: str
	time_val: int
	time_unit: str
