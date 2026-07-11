from app.retry.policy import RetryPolicy
from app.models.job import JobStatus


# purely a business logic
# not to be coupled to persistence DB
class RetryService:
	@staticmethod
	def fail(job, error):
		job.retry_count += 1
		job.last_error = error 
		if job.retry_count > job.max_retries:
			# job is dead now
			job.status = JobStatus.DLQ
		else:
			job.status = JobStatus.PENDING
			job.next_retry_at = RetryPolicy.next_retry(job.retry_count)
		return job
