from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.jobs import router as job_router
from app.db.database import Base, engine


Base.metadata.create_all(bind = engine)


app = FastAPI(
	title = "TaskForge",
	version = "1.0"
)


app.include_router(health_router)
app.include_router(job_router)


@app.get("/")
def root():
	return {
		"message": "TaskForge - Distributed Job Scheduler"
	}