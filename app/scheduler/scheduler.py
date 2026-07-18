import threading
import time
from datetime import datetime
from app.db.database import SessionLocal
from app.repository.job_repository import JobRepository 
from app.scheduler.dispatcher import Dispatcher
from app.recovery.worker_monitor import WorkerMonitor
from app.scheduler.leader import LeaderElection
from app.logging.logger import logger
from app.cache.job_cache import JobCache


class Scheduler:
	POLL_INTERVAL = 1

	def start(self):
		thread = threading.Thread(target = self.loop, daemon = True)
		thread.start()

	# endless loop running in threads to dispatch due jobs to dispatcher
	# (WASTEFUL) as polling many a times does nothing and just sleeps
	def loop(self):
		LeaderElection.start()
		while True:
			logger.info("Polling", datetime.utcnow())
			db = SessionLocal()
			try:
				if not LeaderElection.is_leader:
					time.sleep(2)
					continue
				WorkerMonitor.recover(db)
				pending_ids = JobCache.get_pending()
				if pending_ids is None:
					jobs = JobRepository(db).claim_due_jobs()
					JobCache.put_pending([job.id for job in jobs])
				else:
					jobs = [JobCache.get(job_id) for job_id in pending_ids]
				logger.info("Found jobs: ", len(jobs))
				for job in jobs:
					logger.info(job.id, job.status, job.schedule_time)
					# dispatcher should own the transaction
					Dispatcher.dispatch(db, job)
			except Exception as e:
				logger.error(f"Scheduler error: {e}")
			
			db.close()
			time.sleep(self.POLL_INTERVAL)