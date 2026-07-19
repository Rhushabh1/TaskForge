import os 
from datetime import datetime, timedelta
from jose import jwt, JWTError


SECRET = os.getenv("JWT_SECRET", "taskforge-secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRES", 15))


def create_token(user):
	expire = datetime.utcnow() + timedelta(minutes = EXPIRE_MINUTES)
	payload = {"sub": str(user.id),
				"username": user.username,
				"role": user.role,
				"exp": expire}

	return jwt.encode(payload, SECRET, algorithm = ALGORITHM)


def decode(token):
	try:
		return jwt.decode(token, SECRET, algorithms = [ALGORITHM])
	except JWTError:
		return None