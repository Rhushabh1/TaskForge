# TaskForge
Lightweight Distributed Job Scheduling Platform


## Implementation Techstack:
Python		
APIs		- REST & FAST		
SQL 		- for database
Kafka 		- for message queues
Redis 		- for caching
Docker		- to design a webapp multi-container (+ DB, cache, queues)
Scheduler
Worker + Executor
Retries + Dead letter queues
Metrics loggings


## How to Run:
$> docker compose up --build

- for running worker kafka consumer
$> docker compose exec api python -m app.worker.worker

- for running status-logger kafka consumer
$> docker compose exec api python -m app.queue.status_consumer

- visit http://localhost:8000/docs -> for Swagger UI
- visit http://localhost:8000 -> for verifying successful message
- visit http://localhost:8000/health -> for health of API

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
- orphaned jobs = forever RUNNING if the executor crashes midway -> no SUCCESS/FAILED -> better to add worker heartbeats so that it FAILED if heartbeat timeout
- if all worker threads are busy, then remaining jobs sit in memory -> so pause kafka polling until threadpool has free workers (backpressure -> pausing polling upstream to avoid memory overload downstream)
- remove polling scheduler
- DLQ - dead letter queue
- tracking execution history -> for metrics/analytics
- separate DB commits from repositories and let JobService/UnitOfWork handle it -> rollbacks become easier and there is no inconsistent DB
- only one leader scheduler should dispatch jobs at a time