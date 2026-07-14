from kafka.admin import KafkaAdminClient


admin = KafkaAdminClient(bootstrap_servers = "kafka:9092")


def list_topics():
	return list(admin.list_topics())