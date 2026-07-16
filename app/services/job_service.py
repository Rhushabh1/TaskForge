from datetime import datetime
from app.models.job import JobStatus
from app.models.dlq import DLQJob
from app.repository.job_repository import JobRepository 
from app.repository.dlq_repository import DLQRepository 
from app.retry.service import RetryService


# modelled around UnitOfWork -> all DBs should be updated at once via service layer only
# makes rollbacks easy and DBs consistent
# owns DB commits -> should ideally be the only one committing
class JobService:
	def __init__(self, db):
		self.db = db
		self.job_repo = JobRepository(db)
		self.dlq_repo = DLQRepository(db)

	def handle_execution(self, event):
		job = self.job_repo.get(event["job_id"])
		if job is None:
			return

		job.status = event["status"]
		job.worker_id = event["worker_id"]
		if job.status == JobStatus.SUCCESS:
			job.last_error = None
			job.completed_at = datetime.utcnow()
		elif job.status == JobStatus.FAILED:
			job = RetryService.fail(job, event["output"])
			if job.status == JobStatus.DLQ:
				# update DLQ table as well
				dlq = DLQJob(job_id = job.id,
							failed_at = datetime.utcnow(),
							reason = event["output"])
				self.dlq_repo.create(dlq)
				print("created dlq entry", datetime.utcnow())
		self.db.commit()