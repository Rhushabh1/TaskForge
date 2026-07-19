from app.auth.hashing import verify_password
from app.auth.jwt import create_token, create_refresh_token

from app.repository.user_repository import UserRepository 
from app.monitoring.logger import logger
from app.models.refresh_token import RefreshToken 
from app.repository.refresh_token_repository import RefreshTokenRepository


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
		# return create_token(user)
		access = create_token(user)
		refresh = create_refresh_token()
		RefreshTokenRepository(db).save(
				RefreshToken(token = refresh,
							user_id = user.id,
							expires_at = datetime.utcnow() + timedelta(days = 7))	
			)
		return {"access_token": access,
				"refresh_token": refresh,
				"token_type": "bearer"}