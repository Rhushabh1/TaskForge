import time 
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Histogram
from app.monitoring.exporter import update_metrics
from app.monitoring.correlation import correlation_id


REQUEST_TIME = Histogram("taskforge_request_latency_seconds",
						"Request latency",
						["method", "endpoint"])


class MetricsMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request, call_next):
		start = time.time()
		response = await call_next(request)
		elapsed = time.time() - start 
		REQUEST_TIME.labels(request.method,
							request.url.path
					).observe(elapsed)
		update_metrics()
		return response