from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, DateTime, Enum as SqlEnum
from app.db.database import Base


# for consistent worker status
class WorkerStatus(str, Enum):
	RUNNING = "RUNNING"
	ONLINE = "ONLINE"
	OFFLINE = "OFFLINE"


class Worker(Base):
	__tablename__ = "workers"
	id = Column(Integer,
				primary_key = True,
				index = True)
	hostname = Column(String, 
						unique = True, 
						nullable = False)
	status = Column(SqlEnum(WorkerStatus),
					default = WorkerStatus.OFFLINE,
					nullable = False)
	# same as last seen
	last_heartbeat = Column(DateTime, default = datetime.utcnow)
	# foreign key of job_id
	running_jobs = Column(Integer)