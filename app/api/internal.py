# operational & debugging endpoints
# expose state, metrics, worker info, execution history, kafka topics, scheduler state

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.repository.job_repository import JobRepository
from app.repository.execution_repository import ExecutionRepository 
from app.repository.worker_repository import WorkerRepository 
from app.repository.event_repository import EventRepository 
from app.repository.dlq_repository import DLQRepository 

from app.queue.admin import list_topics
from app.monitoring.metrics import Metrics


router = APIRouter(prefix = "/internal",
					tags = ["Internal Monitoring"])
job_repo = JobRepository(db)
worker_repo = WorkerRepository(db)
exec_repo = ExecutionRepository(db)
dlq_repo = DLQRepository(db)
event_repo = EventRepository(db)


@router.get("/workers")
def workers(db: Session = Depends(get_db)):
	return worker_repo.get_all()


@router.get("/jobs")
def jobs(db: Session = Depends(get_db)):
	return job_repo.get_all()


@router.get("/jobs/pending")
def pending_jobs(db: Session = Depends(get_db)):
	return job_repo.get_pending()


@router.get("/executions")
def executions(db: Session = Depends(get_db)):
	return exec_repo.latest()


@router.get("/executions/failed")
def failed_exec(db: Session = Depends(get_db)):
	return exec_repo.failed()


@router.get("/dlq")
def dlq(db: Session = Depends(get_db)):
	return dlq_repo.get_all()


@router.get("/events")
def events(db: Session = Depends(get_db)):
	return event_repo.latest()


@router.get("/metrics")
def metrics():
	return Metrics.snapshot()


@router.get("/kafka/topics")
def kafka_topics():
	return {"topics": list_topics()}


@router.get("/scheduler")
def scheduler():
	return {"jobs_dispatched": Metrics.scheduler_dispatches}


@router.get("/worker-stats")
def worker_stats():
	return {
		"running": Metrics.worker_running,
		"completed": Metrics.worker_completed
	}