from sqlalchemy.orm import Session
from app.models.job import Job


class JobRepository:
	def __init__(self, db: Session):
		self.db = db

	# create a new job with given Job object
	def create(self, job: Job):
		self.db.add(job)
		self.db.commit()
		self.db.refresh(job)
		return job

	# fetch job for job_id
	def get(self, job_id: int):
		return self.db.query(Job).filter(Job.id == job_id).first()

	# fetch all jobs from the db
	def list(self):
		return self.db.query(Job).all()

	def delete(self, job_id: int):
		job = self.get(job_id)
		if job is None:
			# job_id not found
			return False
		self.db.delete(job)
		self.db.commit()
		return True


