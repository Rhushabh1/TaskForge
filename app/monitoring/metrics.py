from threading import Lock


class Metrics:
	# not to confuse between the 2 locks
	_lock = Lock()
	jobs_created = 0
	jobs_completed = 0
	jobs_failed = 0
	retries = 0
	dlq = 0
	scheduler_dispatches = 0
	worker_running = 0
	worker_completed = 0


	# for incrementing any of the fields above
	# endpoint for metrics update
	@classmethod
	def increment(cls, field):
		with cls._lock:
			setattr(cls, field, getattr(cls, field) + 1)


	@classmethod
	def snapshot(cls):
		return {
			"jobs_created": cls.jobs_created,
			"jobs_completed": cls.jobs_completed,
			"jobs_failed": cls.jobs_failed,
			"retries": cls.retries,
			"dead_letter_jobs": cls.dlq,
			"scheduler_dispatches": cls.scheduler_dispatches,
			"worker_running": cls.worker_running,
			"worker_completed": cls.worker_completed,
		}
