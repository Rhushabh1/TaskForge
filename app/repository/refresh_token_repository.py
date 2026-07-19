from app.models.refresh_token import RefreshToken 
from app.repository.base_repository import BaseRepository 


class RefreshTokenRepository:
	def __init__(self, db):
		self.db = db

	def get_token(self, token):
		return (self.db.query(RefreshToken)
				.filter(RefreshToken.token == token)
				.first())

	def revoke(self, token):
		obj = self.get_token(token)
		if obj:
			self.delete(obj)

	def revoke_user(self, user_id):
		(self.db.query(RefreshToken)
			.filter(RefreshToken.user_id == user_id)
			.delete())
		self.db.commit()

	def delete(self, obj):
		self.db.delete(obj)
		self.db.commit()
		return obj