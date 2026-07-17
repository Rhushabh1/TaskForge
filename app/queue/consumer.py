from app.queue.kafka import create_consumer
from app.queue.topics import JOB_EXECUTE
from app.logging.logger import logger


logger.info("creating consumer")
consumer = create_consumer(JOB_EXECUTE)
logger.info(f"listening on topic: {JOB_EXECUTE}")


for message in consumer:
	logger.info("received message")
	logger.info(message.value)