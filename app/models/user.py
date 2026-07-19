from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from app.db.database import Base


class Roles(str, Enum):
	USER = "USER"
	ADMIN = "ADMIN"


class User(Base):
	__tablename__ = "users"
	id = Column(Integer,
				primary_key = True)
	username = Column(String, 
					unique = True,
					nullable = False)
	email = Column(String, 
					unique = True)
	password_hash = Column(String, 
							nullable = False)
	role = Column(SqlEnum(Roles), default = Roles.USER)
	created_at = Column(DateTime, 
						default = datetime.utcnow,
						nullable = False)