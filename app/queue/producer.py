from app.queue.kafka import producer
from app.queue.topics import JOB_EXECUTE
import uuid


class JobProducer:
	@staticmethod
	def publish(job):
		# need unique event IDs for idempotency (kafka delivers atleast once) 
		# - workers may receive same message twice -> hence unique event IDS
		# attempts -> for retry purposes later
		producer.send(JOB_EXECUTE,
						{
							"event_id": str(uuid.uuid4()),
							"job_id": job.id,
							"job_type": job.job_type,
							"command": job.command,
							"attempt": 0
						}
					)
		producer.flush()