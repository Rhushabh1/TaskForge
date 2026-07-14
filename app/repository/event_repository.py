from sqlalchemy.orm import Session
from app.models.event import ProcessedEvent
from datetime import datetime


class EventRepository:
	def __init__(self, db: Session):
		self.db = db

	# solves duplicate kafka messages
	def already_processed(self, event_id):
		return (self.db.query(ProcessedEvent)
				.filter(ProcessedEvent.id == event_id)
				.first() is not None)

	def save_event(self, event_id):
		event = ProcessedEvent(id = event_id,
								processed_at = datetime.utcnow())
		self.db.add(event)
		self.db.commit()
		self.db.refresh(event)