from pydantic import BaseModel

class AuthBase(BaseModel):
    pass

class TokenResponse(AuthBase):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"