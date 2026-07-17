from app.queue.kafka import get_producer
from app.queue.topics import JOB_EXECUTE
import uuid
from app.logging.logger import logger


class JobProducer:
	@staticmethod
	def publish(job):
		# need unique event IDs for idempotency (kafka delivers atleast once) 
		# - workers may receive same message twice -> hence unique event IDS
		# attempts -> for retry purposes later
		producer = get_producer()
		logger.info(f"publishing to kafka: JOB_EXECUTE")
		producer.send(JOB_EXECUTE,
						{
							"event_id": str(uuid.uuid4()),
							"job_id": job.id,
							"job_type": job.job_type,
							"command": job.command,
							"attempt": job.retry_count + 1
						}
					)
		producer.flush()