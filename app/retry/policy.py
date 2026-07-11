from datetime import datetime, timedelta


class RetryPolicy:
	BASE_DELAY = 2
	@staticmethod
	def next_retry(retry_count):
		delay = RetryPolicy.BASE_DELAY ** retry_count
		return datetime.utcnow() + timedelta(seconds = delay)