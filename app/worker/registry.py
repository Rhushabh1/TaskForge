from datetime import datetime, timedelta

from app.db.database import SessionLocal
from app.models.worker import Worker


ALIVE_THRESHOLD = 20


class WorkerRegistry:
	@staticmethod
	def get_online_workers():
		db = SessionLocal()
		threshold = datetime.utcnow() - timedelta(seconds = ALIVE_THRESHOLD)
		workers = (db.query(Worker)
					.filter(Worker.last_heartbeat >= threshold)
					.all())
		db.close()
		return workers