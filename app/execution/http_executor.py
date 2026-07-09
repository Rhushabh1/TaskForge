import requests
from app.execution.base import BaseExecutor


class HttpExecutor(BaseExecutor):
	def execute(self, url: str):
		response = requests.get(url)
		return {
			"status": response.status_code,
			"body": response.text
		}