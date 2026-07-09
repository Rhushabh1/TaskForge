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

- visit http://localhost:8000/docs -> for Swagger UI
- visit http://localhost:8000 -> for verifying successful message
- visit http://localhost:8000/health -> for health of API

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
- solve duplicate scheduler dispatch bug with each API instance -> add locks when one scheduler is dispatching jobs (classic race condition in distributed scheduler system)
- remove polling scheduler -> move to redis, kafka, listen/notify, zookeeper
- add Kafka
- add Workers
- add Retries
