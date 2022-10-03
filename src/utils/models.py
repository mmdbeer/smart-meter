from pydantic import BaseModel

class Input(BaseModel):
	start: str
	end: str
	var: str
