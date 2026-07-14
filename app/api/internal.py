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


