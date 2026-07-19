from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import decode_token
from app.models.user import Roles


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
	payload = decode_token(token)
	if payload is None:
		raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
							detail = "Invalid token")
	return payload
	# # load the actual user object (instead of payload)
	# user = UserRepository(db).get(int(payload["sub"]))
	# return user


def require_admin(user = Depends(get_current_user)):
	if user["role"] != Roles.ADMIN:
		raise HTTPException(status_code = 403,
							detail = "Admin access required")
	return user