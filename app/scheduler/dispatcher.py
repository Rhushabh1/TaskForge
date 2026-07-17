# temporary dispatcher until the kafka is implemented
from app.queue.producer import JobProducer
from app.models.job import JobStatus
from app.monitoring.metrics import Metrics
from app.logging.logger import logger


class Dispatcher:
	@staticmethod
	def dispatch(db, job):
		logger.info(f"Dispatching job {job.id}")
		job.status = JobStatus.QUEUED
		db.commit()
		JobProducer.publish(job)
		Metrics.increment("scheduler_dispatches")
		logger.info(f"dispatched {job.id}")