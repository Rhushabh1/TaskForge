from fastapi import FastAPI
from app.api.health import router


app = FastAPI(
	title = "TaskForge",
	version = "1.0"
)


app.include_router(router)


@app.get("/")
def root():

	return {
		"message": "TaskForge - Distributed Job Scheduler"
	}