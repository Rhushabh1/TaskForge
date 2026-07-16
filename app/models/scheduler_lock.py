from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base 


class SchedulerLock(Base):
	__tablename__ = "scheduler_lock"
	id = Column(Integer,
				primary_key = True)
	leader = Column(String, 
					nullable = True)
	expires_at = Column(DateTime)
	updated_at = Column(DateTime,
						default = datetime.utcnow,
						onupdate = datetime.utcnow)