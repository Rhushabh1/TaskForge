from datetime import datetime
from app.models.job import Job, JobStatus
from app.repository.base_repository import BaseRepository
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.monitoring.metrics import Metrics
from app.monitoring.logger import logger
from app.cache.job_cache import JobCache


class JobRepository:
	def __init__(self, db: Session):
		self.db = db

	# create a new job with given Job object
	def create(self, job: Job):
		self.db.add(job)
		self.db.commit()
		self.db.refresh(job)
		return job

	# fetch job for job_id
	def get(self, job_id: int):
		return  self.db.query(Job).filter(Job.id == job_id).first()

	# fetch all jobs from the db
	def get_all(self):
		return self.db.query(Job).all()

	def delete(self, job_id: int):
		job = self.get(job_id)
		if job is None:
			# job_id not found
			return False
		self.db.delete(job)
		self.db.commit()
		return True

	# fetching due jobs for the scheduler to dispatch
	# combines get_due_jobs() and mark_queued()
	def claim_due_jobs(self, limit = 20):
		logger.warning(datetime.utcnow())
		# locking the rows to avoid duplicate 
		return (self.db.query(Job)
				.filter(Job.status == JobStatus.PENDING,
					or_(Job.schedule_time <= datetime.utcnow(),
						Job.next_retry_at <= datetime.utcnow()) 
					)
				# what if leader changes during dispatch (hence lock rows)
				.with_for_update(skip_locked = True)
				.limit(limit)
				.all()
				)
		# for job in jobs:
		# 	job.status = JobStatus.QUEUED
		# self.db.commit()
		return jobs

	# for updating status in app/queue/status_consumer.py
	def update_status(self, job_id, status):
		logger.warning("updating job status: ", job_id, status)
		job = self.get(job_id)
		if job:
			job.status = status
			self.db.commit()
			logger.info("db changes committed")
			JobCache.invalidate(job.id)

	def get_pending(self):
		return (self.db.query(Job)
				.filter(Job.status == JobStatus.PENDING, 
						Job.schedule_time <= datetime.utcnow())
				.all())

	def get_running(self):
		return (self.db.query(Job)
				.filter(Job.status == JobStatus.RUNNING)
				.all())

	def get_failed(self):
		return (self.db.query(Job)
				.filter(JobStatus == JobStatus.FAILED)
				.all())

	def recover_jobs(self, worker_id):
		jobs = (self.db.query(Job)
				.filter(Job.worker_id == worker_id,
						Job.status == JobStatus.RUNNING)
				.all())

		for job in jobs:
			job.status = JobStatus.PENDING 
			job.worker_id = None
			job.next_retry_at = datetime.utcnow()
			job.retry_count += 1
			Metrics.increment("retries")
			JobCache.invalidate(job.id)
		
		self.db.commit()
		return jobs

	def assign_worker(self, job, worker):
		job.worker_id = worker.id 
		job.status = JobStatus.RUNNING 
		self.db.commit()


