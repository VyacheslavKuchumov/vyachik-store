from datetime import datetime, timedelta, timezone
from app.config import Settings
import jwt

settings = Settings()

class AuthController:
    def create_access_token(data: dict, expires_delta: timedelta = settings.ACCESS_TOKEN_EXPIRE_MINUTES):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=5)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(data: dict, expires_delta: timedelta = settings.REFRESH_TOKEN_EXPIRE_MINUTES):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def decode_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        
