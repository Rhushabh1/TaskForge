from app.execution.factory import ExecutorFactory
from app.worker.status_publisher import StatusPublisher 


def execute_job(message):
	print("executing jobs: ", message)
	try:
		# alert that job is now running
		StatusPublisher.publish(message["job_id"], "RUNNING")
		executor = ExecutorFactory.get(message["job_type"])
		result = executor.execute(message["command"])
		StatusPublisher.publish(message["job_id"], "SUCCESS", result)
	except Exception as e:
		print("worker error: ", str(e))
		StatusPublisher.publish(message["job_id"], "FAILED", str(e))