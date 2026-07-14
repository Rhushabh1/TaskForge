from fastapi import APIRouter


router = APIRouter()


# minimal liveness -> fast & not depended on expensive checks
@router.get("/health")
def health():
	return {
		"status": "healthy",
		"service": "taskforge-api",
	}