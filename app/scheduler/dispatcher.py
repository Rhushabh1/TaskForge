# temporary dispatcher until the kafka is implemented
from app.queue.producer import JobProducer
from app.models.job import JobStatus
from app.monitoring.metrics import Metrics
from app.monitoring.logger import logger
from app.cache.job_cache import JobCache


class Dispatcher:
	@staticmethod
	def dispatch(db, job):
		logger.info("Dispatching job %s", job.id)
		job.status = JobStatus.QUEUED
		db.commit()
		JobProducer.publish(job)
		Metrics.increment("scheduler_dispatches")
		logger.info("Dispatched job %s", job.id)
		JobCache.invalidate(job.id)