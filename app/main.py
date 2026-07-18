from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.jobs import router as job_router
from app.db.database import Base, engine
import app.models
from app.scheduler.scheduler import Scheduler
# since scheduler starts before fastapi startup finishes
from contextlib import asynccontextmanager
from prometheus_client import make_asgi_app
from app.monitoring.middleware import MetricsMiddleware


Base.metadata.create_all(bind = engine)


# right now every API instance will create a scheduler
# (BUG) can lead to duplicate async dispatch -> duplicate execution
scheduler = Scheduler()

# making sure scheduler starts only after fastapi startup finishes
@asynccontextmanager
async def lifespan(app: FastAPI):
	scheduler.start()
	yield


app = FastAPI(
	title = "TaskForge",
	version = "1.0",
	lifespan = lifespan
)


app.include_router(health_router)
app.include_router(job_router)


# for prometheus monitoring
app.add_middleware(MetricsMiddleware)
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
def root():
	return {
		"message": "TaskForge - Distributed Job Scheduler"
	}