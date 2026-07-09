from fastapi import APIRouter, Depends, HTTPException
# for error handling too

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.job import Job
from app.repository.job_repository import JobRepository 
from app.schemas.job import JobCreate, JobResponse


router = APIRouter(prefix = "/jobs", tags = ["Jobs"])


# depends on successful db session
@router.post("/", response_model = JobResponse)
def create_job(request: JobCreate, db: Session = Depends(get_db)):
	repo = JobRepository(db)
	job = Job(name = request.name,
				command = request.command,
				schedule_time = request.schedule_time)
	return repo.create(job)


# returning list of Jobs
@router.get("/", response_model = list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
	repo = JobRepository(db)
	return repo.list()


@router.get("/{job_id}", response_model = JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
	repo = JobRepository(db)
	job = repo.get(job_id)
	if job is None:
		raise HTTPException(status_code = 404, detail = f"Job {job_id} not found")
	return job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
	repo = JobRepository(db)
	deleted = repo.delete(job_id)
	if not deleted:
		raise HTTPException(status_code = 404, detail = f"Job {job_id} not found")
	return {"message": f"deleted {job_id}"}
