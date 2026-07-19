from app.models.user import User
from app.repository.base_repository import BaseRepository 


class UserRepository:
	def __init__(self, db):
		self.db = db

	def get_by_username(self, username):
		return (self.db.query(User)
				.filter(User.username == username)
				.first())

	def get_by_email(self, email):
		return (self.db.query(User)
				.filter(User.email == email)
				.first())

	def create(self, obj):
		self.db.add(obj)
		self.db.commit()
		self.db.refresh(obj)
		return obj