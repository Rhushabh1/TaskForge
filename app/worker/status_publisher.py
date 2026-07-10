from app.queue.kafka import producer
from app.queue.topics import JOB_STATUS


class StatusPublisher:
	@staticmethod
	def publish(job_id, status, output = None):
		producer.send(JOB_STATUS,
						{
							"job_id": job_id,
							"status": status,
							"output": output
						}
					)
		producer.flush()