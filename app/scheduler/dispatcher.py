# temporary dispatcher until the kafka is implemented
# just print that it has been published to kafka
from app.queue.producer import JobProducer


class Dispatcher:
	@staticmethod
	def dispatch(job):
		print(f"Dispatching job {job.id}")
		JobProducer.publish(job)