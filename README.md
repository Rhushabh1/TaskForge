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

## Requirements file:
$> pip freeze > requirements.txt
$> pip install -r requirements.txt

## TODO:
- add Scheduler
- add Kafka
- add Workers
- add Retries
