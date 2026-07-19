from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
	username: str 
	email = EmailStr
	password = str 


class LoginRequest(BaseModel):
	username: str 
	password: str 


class TokenResponse(BaseModel):
	access_token: str 
	refresh_token: str
	token_type: str = "bearer"


class UserReponse(BaseModel):
	id: int
	username: str 
	email: EmailStr
	role: str 

	class Config:
		from_attributes = True


class RefreshRequest(BaseModel):
	refresh_token: str