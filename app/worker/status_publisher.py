from app.queue.kafka import get_producer
from app.queue.topics import JOB_STATUS
import uuid


class StatusPublisher:
	@staticmethod
	def publish(job_id, status, worker_id, output = None):
		producer = get_producer()
		print(f"publishing to kafka: JOB_STATUS")
		producer.send(JOB_STATUS,
						{
							"event_id": str(uuid.uuid4()),
							"job_id": job_id,
							"status": status,
							"output": output,
							"worker_id": worker_id
						}
					)
		producer.flush()