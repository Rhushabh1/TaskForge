from app.repository.worker_repository import WorkerRepository 
from app.repository.job_repository import JobRepository 
from app.monitoring.logger import logger


class WorkerMonitor:
	@staticmethod
	def recover(db):
		worker_repo = WorkerRepository(db)
		job_repo = JobRepository(db)
		dead_workers = worker_repo.get_dead_workers()
		for worker in dead_workers:
			logger.warning("worker %s: offline", worker.hostname)
			worker_repo.mark_dead(worker)
			jobs = job_repo.recover_jobs(worker.id)
			logger.warning("worker %s: jobs recovered: %s", worker.hostname, len(jobs))