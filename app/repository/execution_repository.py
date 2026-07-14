from sqlalchemy.orm import Session
from app.models.execution import Execution
from app.models.job import JobStatus
from datetime import datetime


class ExecutionRepository:
	def __init__(self, db: Session):
		self.db = db

	# create a new entry with given Execution object
	def create(self, execution: Execution):
		self.db.add(execution)
		self.db.commit()
		self.db.refresh(execution)
		return execution

	# fetch execution for exec_id
	def get(self, exec_id: int):
		return self.db.query(Execution).filter(Execution.id == exec_id).first()

	# fetch all executions from the db
	def latest(self, limit = 50):
		return (self.db.query(Execution)
				.order_by(Execution.started_at.desc())
				.limit(limit)
				.all())

	def failed(self, limit = 20):
		return (self.db.query(Execution)
				.filter(Execution.status == JobStatus.FAILED)
				.order_by(Execution.started_at.desc())
				.limit(limit)
				.all())


