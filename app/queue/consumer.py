from app.queue.kafka import create_consumer
from app.queue.topics import JOB_EXECUTE


print("creating consumer")
consumer = create_consumer(JOB_EXECUTE)
print(f"listening on topic: {JOB_EXECUTE}")


for message in consumer:
	print("received message")
	print(message.value)