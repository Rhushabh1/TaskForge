import requests
from app.execution.base import BaseExecutor


class HttpExecutor(BaseExecutor):
	def execute(self, url: str):
		response = requests.get(url)
		return {
			"return_code": response.status_code,
			"stdout": response.text
		}