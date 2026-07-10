# call task.py -> execute_job()
# replaces consumer.py functionally
from app.queue.kafka import create_consumer
from app.queue.topics import JOB_EXECUTE
from app.worker.task import execute_job
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(max_workers = 4)


print("creating worker")
consumer = create_consumer(JOB_EXECUTE)
print("worker started")
print(f"listening on topic: {JOB_EXECUTE}")


for message in consumer:
	# each kafka message becomes one thread (max 4)
	# runs execute_job(message.value)
	print("received: ", message.value)
	executor.submit(execute_job, message.value)
