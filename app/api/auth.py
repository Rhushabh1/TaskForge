from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import *
from app.models.user import User
from app.repository.user_repository import UserRepository 
from app.auth.hashing imoprt hash_password
from app.auth.service import AuthService

router = APIRouter(prefix = "/auth",
					tags = ["Authentication"])


@router.post("/register", response_model = UserResponse)
def register(request: UserCreate, db: Session = Depends(get_db)):
	user_repo = UserRepository(db)
	if user_repo.get_by_username(request.username):
		raise HTTPException(400, "username already exists")

	user = User(username = request.username,
				email = request.email,
				password_hash = hash_password(request.password))
	return user_repo.create(user)


@router.post("/login", response_model = TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
	token = AuthService.authenticate(db, request.username, request.password)
	if token is None:
		raise HTTPException(401, "Invalid credentials")

	return {"access_token": token,
			"token_type": "bearer"}