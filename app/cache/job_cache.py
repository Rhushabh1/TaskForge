import json
from app.cache.redis_client import redis_client
from app.monitoring.metrics import Metrics


# redis shouldn't leak everywhere
# only GET for cache-aside pattern
class JobCache:
	# TTL = time to live
	CACHE_TTL = 300

	@staticmethod
	def get(job_id):
		value = redis_client.get(f"job:{job_id}")
		if value:
			# cache HIT
			Metrics.increment("cache_hits")
			return json.loads(value)

		# cache MISS
		Metrics.increment("cache_misses")
		return None

	@staticmethod
	def put(job):
		redis_client.setex(f"job:{job.id}",
							CACHE_TTL,
							json.dumps({"id": job.id,
										"status": job.status,
										"retry": job.retry_count})
							)

	# whenever cache data becomes stale (don't update, just invalidate)
	@staticmethod
	def invalidate(job_id):
		redis_client.delete(f"job:{job_id}")


	@staticmethod
	def get_pending():
		return None

	@staticmethod
	def put_pending(pending_ids):
		pass