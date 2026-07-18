from app.monitoring.metrics import Metrics
from app.monitoring.prometheus_metrics import *


def update_metrics():
	snapshot = Metrics.snapshot()
	
	jobs_created.set(snapshot["jobs_created"])
	jobs_completed.set(snapshot["jobs_completed"])
	jobs_failed.set(snapshot["jobs_failed"])
	retries.set(snapshot["retries"])
	dead_letter_jobs.set(snapshot["dead_letter_jobs"])
	scheduler_dispatches.set(snapshot["scheduler_dispatches"])
	worker_running.set(snapshot["worker_running"])
	worker_completed.set(snapshot["worker_completed"])
	cache_hits.set(snapshot["cache_hits"])
	cache_misses.set(snapshot["cache_misses"])