from datetime import datetime
from pydantic import BaseModel


class JobCreate(BaseModel):
	name: str
	command: str
	schedule_time: datetime


class JobResponse(BaseModel):
	id: int
	name: str
	command: str
	schedule_time: datetime
	status: str
	retry_count: int

	class Config:

		from_attributes = True