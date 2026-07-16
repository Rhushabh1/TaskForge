from datetime import datetime, timedelta
from app.models.scheduler_lock import SchedulerLock 


LEASE_SECONDS = 10 


class SchedulerLockRepository:
	def __init__(self, db):
		self.db = db
		# insert row with (id = 1, leader = NULL, expires_at = now)
		lock = SchedulerLock(id = 1,
							leader = None, 
							expires_at = datetime.utcnow())
		self.save(lock)

	def save(self, lock):
		self.db.add(lock)
		self.db.commit()
		self.db.refresh(lock)
		return lock

	def get(self, id):
		return (self.db.query(SchedulerLock)
				.filter(SchedulerLock.id == id)
				.first())

	def acquire(self, scheduler_name):
		lock = self.get(1)
		now = datetime.utcnow()
		# tries to acquire the lock (no matter who held it before this)
		if (lock.expires_at is None) or (lock.expires_at < now):
			lock.leader = scheduler_name
			lock.expires_at = now + timedelta(seconds = LEASE_SECONDS)
			self.db.commit()
			return True

		if lock.leader == scheduler_name:
			return True

		return False

	def renew(self, scheduler_name):
		lock = self.get(1)
		if lock.leader != scheduler_name:
			return False

		lock.expires_at = datetime.utcnow() + timedelta(seconds = LEASE_SECONDS)
		self.db.commit()
		return True

	def leader(self):
		return self.get(1).leader

	def is_leader(self, scheduler_name):
		lock = self.get(1)
		return lock.leader == scheduler_name