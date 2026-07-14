from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


# never overwrite history of executions
class DLQJob(Base):
	__tablename__ = "dead_letter_jobs"
	id = Column(Integer, 
				primary_key = True, 
				index = True)
	job_id = Column(Integer, nullable = False)
	failed_at = Column(DateTime,
						default = datetime.utcnow,
						nullable = False)
	reason = Column(String, nullable = False)