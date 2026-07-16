from app.repository.worker_repository import WorkerRepository 
from app.repository.job_repository import JobRepository 


class WorkerMonitor:
	@staticmethod
	def recover(db):
		worker_repo = WorkerRepository(db)
		job_repo = JobRepository(db)
		dead_workers = worker_repo.get_dead_workers()
		for worker in dead_workers:
			print(f"[Recover] worker {worker.hostname} is dead")
			worker_repo.mark_dead(worker)
			jobs = job_repo.recover_jobs(worker.id)
			print(f"[Recovery] recovered {len(jobs)} jobs")