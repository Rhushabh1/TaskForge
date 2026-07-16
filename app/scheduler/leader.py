import os
import threading
import time

from app.db.database import SessionLocal
from app.repository.scheduler_lock_repository import SchedulerLockRepository 


SCHEDULER_NAME = os.getenv("SCHEDULER_NAME", "scheduler-1")


class LeaderElection:
	is_leader = False

	@classmethod
	def heartbeat(cls):
		while True:
			db = SessionLocal()
			repo = SchedulerLockRepository(db)
			if repo.acquire(SCHEDULER_NAME):
				repo.renew(SCHEDULER_NAME)
				cls.is_leader = True
			else:
				cls.is_leader = False
			
			db.close()
			time.sleep(5)

	@classmethod
	def start(cls):
		threading.Thread(target = cls.heartbeat,
						daemon = True).start()