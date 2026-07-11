from sqlalchemy.orm import Session
from app.models.dlq import DLQJob
from datetime import datetime


class DLQRepository:
	def __init__(self, db: Session):
		self.db = db

	# create a new entry with given dlq job object
	def create(self, dlq_job: DLQJob):
		print("creating dlq_job", datetime.utcnow())
		self.db.add(dlq_job)
		print("before commit", datetime.utcnow())
		self.db.commit()
		print("after commit", datetime.utcnow())
		self.db.refresh(dlq_job)
		print("id", dlq_job.id, datetime.utcnow())
		return dlq_job

	# fetch dlq job for dlq_id
	def get(self, dlq_id: int):
		return self.db.query(DLQJob).filter(DLQJob.id == dlq_id).first()

	# fetch all dlq jobs from the db
	def list(self):
		return self.db.query(DLQJob).all()

	# likely never used
	def delete(self, dlq_id: int):
		dlq_job = self.get(dlq_id)
		if dlq_job is None:
			# dlq_id not found
			return False
		self.db.delete(dlq_job)
		self.db.commit()
		return True


