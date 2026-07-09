import threading
import time
from datetime import datetime
from app.db.database import SessionLocal
from app.repository.job_repository import JobRepository 
from app.scheduler.dispatcher import Dispatcher


class Scheduler:
	POLL_INTERVAL = 1
	def start(self):
		thread = threading.Thread(target = self.loop, daemon = True)
		thread.start()

	# endless loop running in threads to dispatch due jobs to dispatcher
	# (WASTEFUL) as polling many a times does nothing and just sleeps
	def loop(self):
		while True:
			print("Polling", datetime.utcnow())
			db = SessionLocal()
			try:
				repo = JobRepository(db)
				jobs = repo.claim_due_jobs()
				print("Found jobs: ", len(jobs))
				for job in jobs:
					print(job.id, job.status, job.schedule_time)
					Dispatcher.dispatch(job)
			except Exception as e:
				print(f"Scheduler error: {e}")
			finally:
				db.close()
			time.sleep(self.POLL_INTERVAL)