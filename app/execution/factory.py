from app.execution.shell_executor import ShellExecutor 
from app.execution.python_executor import PythonExecutor 
from app.execution.http_executor import HttpExecutor 


class ExecutorFactory:
	@staticmethod
	def get(job_type: str):
		if job_type == "shell":
			return ShellExecutor()
		elif job_type == "python":
			return PythonExecutor()
		elif job_type == "http":
			return HttpExecutor()
		else:
			raise Exception("Unknown job type")