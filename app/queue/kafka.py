from kafka import KafkaProducer, KafkaConsumer
import json
import time
from app.monitoring.logger import logger


_producer = None

def get_producer():
	global _producer
	if _producer is not None:
		return _producer

	while True:
		try:
			logger.info("connecting to kafka")
			_producer = KafkaProducer(bootstrap_servers = "kafka:9092",
						value_serializer = lambda v: json.dumps(v).encode())
			logger.info("connected to kafka")
			return _producer
		except Exception as e:
			logger.error(f"kafka not ready: {e}")
			time.sleep(5)


def create_consumer(topic):
	while True:
		try:
			return KafkaConsumer(topic,
								bootstrap_servers = "kafka:9092",
								value_deserializer = lambda v: json.loads(v.decode()),
								auto_offset_reset = "earliest",
								enable_auto_commit = True,
								group_id = "TaskForge")
		except Exception as e:
			logger.error(f"waiting for kafka consumer: {e}")
			time.sleep(5)
