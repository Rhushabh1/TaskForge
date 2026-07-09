# temporary dispatcher until the kafka is implemented
# just print that it has been published to kafka

class Dispatcher:
	@staticmethod
	def dispatch(job):
		print(f"Dispatching job {job.id}")
		return True