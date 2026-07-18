import logging
import structlog


logging.basicConfig(level = logging.INFO,
					format = "%(message)s")


logger = structlog.get_logger()

# logger.info(
#     "job started",
#     job_id=15,
#     worker="worker-2"
# )