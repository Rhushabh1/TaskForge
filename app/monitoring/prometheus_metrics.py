from prometheus_client import Gauge


jobs_created = Gauge("taskforge_jobs_created",
					"Total jobs created")

jobs_completed = Gauge("taskforge_jobs_completed",
					"Total jobs completed")

jobs_failed = Gauge("taskforge_jobs_failed",
					"Total jobs failed")

retries = Gauge("taskforge_job_retries",
				"Total retries")

dead_letter_jobs = Gauge("taskforge_dead_letter_jobs",
						"Jobs moved to DLQ")

scheduler_dispatches = Gauge("taskforge_scheduler_dispatches",
							"Scheduler dispatch count")

worker_running = Gauge("taskforge_worker_running",
						"Running jobs")

worker_completed = Gauge("taskforge_worker_completed",
						"Completed jobs")

cache_hits = Gauge("taskforge_cache_hits",
					"Redis cache hits")

cache_misses = Gauge("taskforge_cache_misses",
					"Redis cache misses")