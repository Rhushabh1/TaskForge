from sqlalchemy.orm import Session
from app.repository.job_repository import JobRepository
from app.repository.worker_repository import WorkerRepository
from app.repository.execution_repository import ExecutionRepository
from app.repository.event_repository import EventRepository
from app.repository.dlq_repository import DLQRepository


# to tackle large repository mgmt
class Repository:
	def __init__(self, db: Session):
		self.jobs = JobRepository(db)
		self.workers = WorkerRepository(db)
		self.executions = ExecutionRepository(db)
		self.events = EventRepository(db)
		self.dlq = DLQRepository(db)


# HOW TO USE:
# repo = Repository(db)
# repo.jobs.get_running()
# repo.workers.get(worker_id)
