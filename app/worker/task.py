from datetime import datetime
from app.db.database import SessionLocal
from app.models.execution import Execution
from app.repository.event_repository import EventRepository
from app.repository.execution_repository import ExecutionRepository

from app.execution.factory import ExecutorFactory
from app.worker.status_publisher import StatusPublisher
from app.models.job import JobStatus


def execute_job(message):
	print("executing jobs: ", message)

	# connect to execution db
	db = SessionLocal()
	exec_repo = ExecutionRepository(db)
	event_repo = EventRepository(db)
	# to check for duplicate event_ids
	if event_repo.already_processed(message["event_id"]):
		return 
	# alert that job is now running
	StatusPublisher.publish(message["job_id"], JobStatus.RUNNING)
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
		StatusPublisher.publish(message["job_id"], JobStatus.SUCCESS)
	except Exception as e:
		print("worker error: ", str(e))
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
		StatusPublisher.publish(message["job_id"], JobStatus.FAILED, str(e))
	finally:
		event_repo.save_event(message["event_id"])
		db.close()