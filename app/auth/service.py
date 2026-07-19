from app.auth.hashing import verify_password
from app.auth.jwt import create_token

from app.repository.user_repository import UserRepository 
from app.monitoring.logger import logger


class AuthService:
	@staticmethod
	def authenticate(db, username, password):
		user_repo = UserRepository(db)
		user = user_repo.get_by_username(username)
		if not user:
			logger.warning("login failed: username - %s", username)
			return None

		if not verify_password(password, user.password_hash):
			logger.warning("login failed: username - %s", username)
			return None

		logger.info("login user = %s", user.id)
		return create_token(user)