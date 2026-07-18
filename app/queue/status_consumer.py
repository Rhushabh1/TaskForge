from app.queue.kafka import create_consumer
from app.queue.topics import JOB_STATUS
from app.db.database import SessionLocal
from app.repository.job_repository import JobRepository 
from app.services.job_service import JobService
from app.monitoring.logger import logger


logger.info("creating status listener")
consumer = create_consumer(JOB_STATUS)
logger.info(f"listening on topic: {JOB_STATUS}")


# owns jobs, retry, DLQ, metrics, analytics, notifications, etc.
for message in consumer:
	db = SessionLocal()
	try:
		event = message.value
		logger.info("job event: ", event)
		JobService(db).handle_execution(event)
	finally:
		db.close()