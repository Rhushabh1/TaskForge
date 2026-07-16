from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.worker import Worker, WorkerStatus


ALIVE_TIMEOUT = 20


class WorkerRepository:
	def __init__(self, db: Session):
		self.db = db

	def get_all(self):
		return (self.db.query(Worker)
				.order_by(Worker.id)
				.all())

	def heartbeat(self, worker_name):
		worker = (self.db.query(Worker)
					.filter(Worker.hostname == worker_name)
					.first())

		if worker is None:
			worker = Worker(hostname = worker_name)
			self.db.add(worker)

		worker.status = WorkerStatus.ONLINE
		worker.last_heartbeat = datetime.utcnow()
		self.db.commit()
		return worker

	def get_online_workers(self, timeout = ALIVE_TIMEOUT):
		threshold = datetime.utcnow() - timedelta(seconds = timeout)
		return (self.db.query(Worker)
				.filter(Worker.status == WorkerStatus.ONLINE,
						Worker.last_heartbeat >= threshold)
				.all())

	def get_dead_workers(self, timeout = ALIVE_TIMEOUT):
		threshold = datetime.utcnow() - timedelta(seconds = timeout)
		return (self.db.query(Worker)
				.filter(Worker.status == WorkerStatus.ONLINE,
						Worker.last_heartbeat < threshold)
				.all())

	def mark_dead(self, worker):
		worker.status = WorkerStatus.OFFLINE
		self.db.commit()