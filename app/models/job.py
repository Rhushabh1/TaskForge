from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum, ForeignKey
from app.db.database import Base


# for consistent job status across models
class JobStatus(str, Enum):
	PENDING = "PENDING"
	QUEUED = "QUEUED"
	RUNNING = "RUNNING"
	SUCCESS = "SUCCESS"
	FAILED = "FAILED"
	DLQ = "DLQ"


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
	worker_id = Column(Integer,
						ForeignKey("workers.id"),
						nullable = True,
						default = None)
	# will add retry later
	max_retries = Column(Integer,
						default = 3,
						nullable = False)
	retry_count = Column(Integer, 
						default = 0,
						nullable = False)
	# for exponential backoff
	next_retry_at = Column(DateTime, nullable = True)
	last_error = Column(String, nullable = True)
	# setting up automatic update	
	created_at = Column(DateTime, default = datetime.utcnow)
	updated_at = Column(DateTime, 
						default = datetime.utcnow,
						onupdate = datetime.utcnow)

