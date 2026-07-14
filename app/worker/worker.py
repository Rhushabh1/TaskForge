# call task.py -> execute_job()
# replaces consumer.py functionally
import socket
import uuid
import threading
import time

from concurrent.futures import ThreadPoolExecutor

from app.queue.kafka import create_consumer
from app.queue.topics import JOB_EXECUTE
from app.worker.task import execute_job
from app.worker.heartbeat import HeartbeatService


HEARTBEAT_CHECK = 10
MAX_WORKERS = 4
# register each worker container as distinct + easily scalable for multiple workers
WORKER_NAME = f"{socket.gethostname()}-{uuid.uuid4().hex[:6]}"
executor = ThreadPoolExecutor(max_workers = MAX_WORKERS)


def heartbeat_loop():
	while True:
		HeartbeatService.send(WORKER_NAME)
		time.sleep(HEARTBEAT_CHECK)


def start():
	# 1 - create kafka consumer
	# 2 - manage thread pool of executors
	# 3 - run consumer loop
	# 4 - send heartbeats
	# 5 - register worker (TODO)
	# 6 - shutdown gracefully (TODO)
	print(f"starting worker: {WORKER_NAME}")
	threading.Thread(target = heartbeat_loop,
					daemon = True
					).start()
	consumer = create_consumer(JOB_EXECUTE)
	print(f"listening on topic: {JOB_EXECUTE}")
	for message in consumer:
		# each kafka message becomes one thread (max 4)
		# runs execute_job(message.value)
		print(f"received: {message.value}")
		executor.submit(execute_job, message.value)


if __name__ == "__main__":
	start()
