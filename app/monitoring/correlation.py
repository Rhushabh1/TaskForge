import uuid


# generate UUID if client doesn't send correlation_id with request
def correlation_id():
	return str(uuid.uuid4())