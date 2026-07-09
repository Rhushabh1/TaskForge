import subprocess
from app.execution.base import BaseExecutor


class ShellExecutor(BaseExecutor):
	def execute(self, command: str):
		process = subprocess.run(command, 
								shell = True,
								capture_output = True,
								text = True)
		return {
			"stdout": process.stdout,
			"stderr": process.stderr,
			"returncode": process.returncode
		}