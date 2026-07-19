# TaskForge
Lightweight Distributed Job Scheduling Platform


## Implementation Techstack:
Python		
APIs		- REST & FAST		
SQL 		- for database
Kafka 		- for message queues
Redis 		- for caching (repositories should be DB only (persistence), services should own the cache)
Docker		- to design a webapp multi-container (+ DB, cache, queues)
Scheduler
Worker + Executor
Retries + Dead letter queues
Metrics loggings -> human json endpoint + prometheus' openmetrics format


## How to Run:
$> docker compose up --build

- for running worker kafka consumer
$> docker compose exec api python -m app.worker.worker

- for running status-logger kafka consumer
$> docker compose exec api python -m app.queue.status_consumer

- visit http://localhost:8000/docs -> for Swagger UI
- visit http://localhost:8000 -> for verifying successful message
- visit http://localhost:8000/health -> for health of API
- visit http://localhost:8000/metrics -> for prometheus monitoring

- to shutdown everything
$> docker compose down -v

for inspecting TaskForge DB
$>  docker exec -it taskforge-db psql -U TaskForge -d TaskForge


## Docker build issue
when the docker build fails after "docker compose up --build"
- close Docker Desktop
$> taskkill /F /IM "Docker Desktop.exe"
$> taskkill /F /IM "com.docker.backend.exe"
$> Remove-Item "$env:USERPROFILE\.docker\buildx" -Recurse -Force
- restart Docker Desktop
$> docker buildx ls
$> $env:DOCKER_BUILDKIT=0
$> $env:COMPOSE_DOCKER_CLI_BUILD=0
$> docker compose build
$> docker compose up --build

## Requirements file:
$> pip freeze > requirements.txt
$> pip install -r requirements.txt

## Scheduler Logic
it just dispatches jobs, doesn't execute anything
thats the work of the worker
- select jobs where status = pending & time <= current time
- publish to kafka
- status = queued

## TODO:
- if all worker threads are busy, then remaining jobs sit in memory -> so pause kafka polling until threadpool has free workers (backpressure -> pausing polling upstream to avoid memory overload downstream)
- remove polling scheduler
- base_repository.py is not incorporated in the codebase
- create a repository factory which rests in app/repository/__init__.py -> not incorporated in the codebase
- likely move worker heartbeats onto a dedicated kafka topic and process them asynchronously
- adding workers & schedulers to docker-compose.yml 
- invalidate JobCache wherever cache becomes stale -> ie, wherever job.status changes
- CACHE points -> 
		GET Job
		GET Worker
		Pending Job IDs (in scheduler)
		Internal Jobs API
		Internal Worker API
- introduce a service layer -> APIs shouldn't directly talk to repositories
- use alembic for database migrations instead of Base.metadata.create_all()
- centralise config (kafka, redis, db, metrics) into single Settings class
- make kafka publish asynchronously -> so APIs don't block on flush()
- delete app/logging/logger.py -> shift to app/monitoring/logger.py