from app.monitoring.logger import logger
# for error handling too
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.job import Job
from app.repository.job_repository import JobRepository 
from app.schemas.job import JobCreate, JobResponse
# temporary execute API before putting it in scheduler
from app.execution.factory import ExecutorFactory
from app.cache.job_cache import JobCache

from app.auth.dependencies import get_current_user
from app.models.user import Roles


router = APIRouter(prefix = "/jobs", tags = ["Jobs"])
# job_repo = JobRepository(db)


# depends on successful db session
@router.post("/", response_model = JobResponse)
def create_job(request: JobCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
	job_repo = JobRepository(db)
	logger.info("API enters")
	job = Job(name = request.name,
				command = request.command,
				job_type = request.job_type,
				schedule_time = request.schedule_time,
				user_id = int(user["sub"]))
	job = job_repo.create(job)
	JobCache.put(job)
	logger.info("after create API")
	return job


# returning list of Jobs
@router.get("/", response_model = list[JobResponse])
def list_jobs(db: Session = Depends(get_db), user = Depends(get_current_user)):
	job_repo = JobRepository(db)
	return job_repo.get_all(user)


@router.get("/{job_id}", response_model = JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
	job_repo = JobRepository(db)
	job = job_repo.get(job_id)
	if job is None:
		raise HTTPException(status_code = 404, detail = f"Job {job_id} not found")
	return job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
	job_repo = JobRepository(db)
	job = job_repo.get(job_id)
	if (job.user_id != int(user["sub"])) and (user["role"] != Roles.ADMIN):
		raise HTTPException(403, "Forbidden")

	deleted = job_repo.delete(job_id)
	JobCache.invalidate(job_id)
	if not deleted:
		raise HTTPException(status_code = 404, detail = f"Job {job_id} not found")
	return {"message": f"deleted {job_id}"}


# TEST: EXECUTION ENGINE
# temporary execute API before putting it in scheduler
@router.post("/{job_id}/execute")
def execute_job(job_id: int, db: Session = Depends(get_db)):
	job_repo = JobRepository(db)
	job = job_repo.get(job_id)
	if not job:
		raise HTTPException(404, f"Job {job_id} not found")
	executor = ExecutorFactory.get(job.job_type)
	result = executor.execute(job.command)
	return result


# WHO AM I - endpoint check
@router.get("/me")
def me(user = Depends(get_current_user)):
	return user
