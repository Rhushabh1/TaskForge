import subprocess
from app.execution.base import BaseExecutor


class PythonExecutor(BaseExecutor):
	def execute(self, script: str):
		process = subprocess.run(["python", script],
								capture_output = True,
								text = True)
		return {
			"stdout": process.stdout,
			"stderr": process.stderr,
			"returncode": process.returncode
		}