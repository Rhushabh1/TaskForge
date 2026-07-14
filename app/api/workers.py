from fastapi import APIRouter
from app.worker.registry import WorkerRegistry


router = APIRouter(prefix = "/workers", tags = ["Workers"])


@router.get("/workers")
def workers():
	workers = WorkerRegistry.get_online_workers()
	# return [{"worker_name": w.hostname,
	# 			"status": w.status,
	# 			"last_heartbeat": w.last_heartbeat} for w in workers]
	return workers 