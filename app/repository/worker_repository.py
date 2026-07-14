from sqlalchemy.orm import Session
from datetime import datetime
from app.models.worker import Worker, WorkerStatus


class WorkerRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_all(self):
		return (self.db.query(Worker)
				.order_by(Worker.id)
				.all())

	def get_online(self):
		return (self.db.query(Worker)
				.filter(Worker.status == WorkerStatus.ONLINE)
				.all())