from kafka import KafkaProducer, KafkaConsumer
import json


print("before producer")
producer = KafkaProducer(bootstrap_servers = "kafka:9092",
						value_serializer = lambda v: json.dumps(v).encode())
print("producer created")


def create_consumer(topic):
	return KafkaConsumer(topic,
						bootstrap_servers = "kafka:9092",
						value_deserializer = lambda v: json.loads(v.decode()),
						auto_offset_reset = "earliest",
						enable_auto_commit = True,
						group_id = "TaskForge")
