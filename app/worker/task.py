from datetime import datetime
from app.db.database import SessionLocal
from app.models.execution import Execution
from app.repository.event_repository import EventRepository
from app.repository.execution_repository import ExecutionRepository
from app.repository.worker_repository import WorkerRepository

from app.execution.factory import ExecutorFactory
from app.worker.status_publisher import StatusPublisher
from app.models.job import JobStatus
from app.monitoring.metrics import Metrics
from app.logging.logger import logger


def execute_job(message, worker_id):
	logger.info("executing jobs: ", message)

	# connect to execution db
	db = SessionLocal()
	exec_repo = ExecutionRepository(db)
	event_repo = EventRepository(db)
	worker_repo = WorkerRepository(db)

	# to check for duplicate event_ids
	if event_repo.already_processed(message["event_id"]):
		return 
	# alert that job is now running
	Metrics.increment("worker_running")
	StatusPublisher.publish(message["job_id"], JobStatus.RUNNING, worker_id)
	start_time = datetime.utcnow()
	
	try:
		executor = ExecutorFactory.get(message["job_type"])
		result = executor.execute(message["command"])
		# update Execution table
		execution = Execution(job_id = message["job_id"],
							attempt = message["attempt"],
							started_at = start_time,
							ended_at = datetime.utcnow(),
							status = JobStatus.SUCCESS,
							output = result.get("stdout", ""),
							error = result.get("stderr", ""),
							return_code = result.get("return_code", 0))
		exec_repo.create(execution)
		# no need to pass result to publisher -> result is not updated in Job table
		Metrics.increment("jobs_completed")
		StatusPublisher.publish(message["job_id"], JobStatus.SUCCESS, worker_id)
	except Exception as e:
		logger.error("worker error: ", str(e))
		# update Execution table
		execution = Execution(job_id = message["job_id"],
							attempt = message["attempt"],
							started_at = start_time,
							ended_at = datetime.utcnow(),
							status = JobStatus.FAILED,
							output = None,
							error = str(e),
							return_code = 1)
		exec_repo.create(execution)
		Metrics.increment("jobs_failed")
		StatusPublisher.publish(message["job_id"], JobStatus.FAILED, worker_id, str(e))
	finally:
		Metrics.decrement("worker_running")
		Metrics.increment("worker_completed")
		event_repo.save_event(message["event_id"])
		db.close()