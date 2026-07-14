from datetime import datetime
from app.db.database import SessionLocal
from app.models.worker import Worker, WorkerStatus


class HeartbeatService:
	# sends heartbeat to the worker db
	@staticmethod
	def send(worker_name):
		db = SessionLocal()
		worker = (db.query(Worker)
					.filter(Worker.hostname == worker_name)
					.first())

		if worker is None:
			worker = Worker(hostname = worker_name,
							status = WorkerStatus.ONLINE)
			db.add(worker)

		worker.status = WorkerStatus.ONLINE
		worker.last_heartbeat = datetime.utcnow()
		db.commit()
		db.close()
