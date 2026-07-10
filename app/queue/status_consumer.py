from app.queue.kafka import create_consumer
from app.queue.topics import JOB_STATUS
from app.db.database import SessionLocal
from app.repository.job_repository import JobRepository 


print("creating status listener")
consumer = create_consumer(JOB_STATUS)
print("listener started")
print(f"listening on topic: {JOB_STATUS}")


for message in consumer:
	db = SessionLocal()
	repo = JobRepository(db)
	job = message.value
	print("job: ", job)
	repo.update_status(job["job_id"], job["status"])
	db.close()