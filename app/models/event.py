from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.db.database import Base


class ProcessedEvent(Base):
	__tablename__ = "processed_events"
	# UUID is string format
	id = Column(String, 
				primary_key = True)
	processed_at = Column(DateTime, default = datetime.utcnow)