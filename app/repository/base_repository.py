from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Type


class BaseRepository:
	def __init__(self, db: Session, model: Type):
		self.db = db
		self.model = model

# basic CRUD functions
	def get(self, id: int):
		return (self.db.query(self.model)
				.filter(self.model.id == id)
				.first())

	def get_all(self):
		return (self.db.query(self.model)
				.all())

	# or create()
	def save(self, obj):
		self.db.add(obj)
		self.db.commit()
		self.db.refresh(obj)
		return obj

	def refresh(self, obj):
		self.db.refresh(obj)
		return obj

	def delete(self, obj):
		self.db.delete(obj)
		self.db.commit()
		return obj

	def delete_by_id(self, id: int):
		obj = self.get(id)
		if obj:
			self.delete(obj)
		return obj

# query functions
	def latest(self, column = None, limit = 50):
		if column is None:
			column = self.model.id
		return (self.db.query(self.model)
				.order_by(desc(column))
				.limit(limit)
				.all())

	def count(self):
		return (self.db.query(self.model)
				.count())

	def exists(self, id: int):
		return self.get(id) is not None

# db helper functions (no return here)
	def commit(self):
		self.db.commit()

	def flush(self):
		self.db.flush()

	def rollback(self):
		self.db.rollback()

	def close(self):
		self.db.close()
