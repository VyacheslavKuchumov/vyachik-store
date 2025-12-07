# app/schemas/user.py
from pydantic import BaseModel, EmailStr

# Базовая схема с общими полями, которые есть всегда
class UserBase(BaseModel):
    email: EmailStr
    username: str
    
# Схема для регистрации пользователя
class UserSignup(UserBase):
    password: str

# Схема для СОЗДАНИЯ пользователя через админку
class UserCreate(UserBase):
    password: str
    is_superuser: bool = False

# Схема для ОБНОВЛЕНИЯ пользователя через админку
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None

# Схема для ОТВЕТА (Output DTO)
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    
    class Config:
        from_attributes = True