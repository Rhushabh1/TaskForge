from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from app.db.database import Base


# for consistent job status across models
class JobStatus(str, Enum):
	PENDING = "PENDING"
	QUEUED = "QUEUED"
	RUNNING = "RUNNING"
	SUCCESS = "SUCCESS"
	FAILED = "FAILED"
	CANCELLED = "CANCELLED"
	# no retries for now (just basic CRUD)


# model for how a Job object structure looks like
class Job(Base):
	__tablename__ = "jobs"
	id = Column(Integer, 
				primary_key = True, 
				index = True)
	name = Column(String, nullable = False)
	command = Column(String, nullable = False)
	schedule_time = Column(DateTime, nullable = False)
	status = Column(SqlEnum(JobStatus),
					default = JobStatus.PENDING,
					nullable = False)
	job_type = Column(String,
						nullable = False,
						default = "shell")
	# will add retry later
	retry_count = Column(Integer, default = 0)
	created_at = Column(DateTime, default = datetime.utcnow)
	# setting up automatic update	
	updated_at = Column(DateTime, 
						default = datetime.utcnow,
						onupdate = datetime.utcnow)

