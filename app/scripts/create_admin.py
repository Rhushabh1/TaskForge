# run it once using cmd:
# $> python -m app.scripts.create_admin

from app.db.database import SessionLocal
from app.models.user import Roles
from app.repository.user_repository import UserRepository 
from app.auth.hashing import hash_password


db = SessionLocal()
user_repo = UserRepository(db)
if user_repo.get_by_username("admin"):
	print("Admin already exists")
else:
	admin = User(username = "admin",
				email = "admin@taskforge.com",
				password_hash = hash_password("admin123"),
				role = Roles.ADMIN)
	user_repo.create(admin)
	print("Admin created")