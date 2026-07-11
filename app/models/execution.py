from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from app.db.database import Base
from app.models.job import JobStatus


# never overwrite history of executions
class Execution(Base):
	__tablename__ = "executions"
	id = Column(Integer, 
				primary_key = True, 
				index = True)
	job_id = Column(Integer, nullable = False)
	worker_id = Column(Integer, default = 0)
	attempt = Column(Integer, 
					default = 1,
					nullable = False)
	started_at = Column(DateTime, default = datetime.utcnow)
	ended_at = Column(DateTime)
	status = Column(SqlEnum(JobStatus),
					default = JobStatus.RUNNING,
					nullable = False)
	output = Column(String, nullable = True)
	error = Column(String, nullable = True)
	return_code = Column(Integer, nullable = True)