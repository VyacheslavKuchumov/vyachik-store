from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from app.config import Settings
from app.controllers.auth_controller import AuthController

password_hash = PasswordHash.recommended()
settings = Settings()
auth_controller = AuthController()

class UserController:
    def verify_password(plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    def get_password_hash(password):
        return password_hash.hash(password)
    
    def get_current_user(token: str = Depends(settings.OAUTH2_SCHEME)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = auth_controller.decode_token(token)
        if payload is None:
            return None
        return payload.get("sub")
    
    def check_superuser(user):
        # Здесь должна быть логика проверки, является ли пользователь суперпользователем
        return user.get("is_superuser", False)