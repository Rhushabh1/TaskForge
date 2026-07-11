from sqlalchemy.orm import Session
from app.models.execution import Execution
from datetime import datetime


class ExecutionRepository:
	def __init__(self, db: Session):
		self.db = db

	# create a new entry with given Execution object
	def create(self, execution: Execution):
		print("creating execution", datetime.utcnow())
		self.db.add(execution)
		print("before commit", datetime.utcnow())
		self.db.commit()
		print("after commit", datetime.utcnow())
		self.db.refresh(execution)
		print("id", execution.id, datetime.utcnow())
		return execution

	# fetch execution for exec_id
	def get(self, exec_id: int):
		return self.db.query(Execution).filter(Execution.id == exec_id).first()

	# fetch all executions from the db
	def list(self):
		return self.db.query(Execution).all()

	# likely never used
	def delete(self, exec_id: int):
		execution = self.get(exec_id)
		if execution is None:
			# exec_id not found
			return False
		self.db.delete(execution)
		self.db.commit()
		return True


