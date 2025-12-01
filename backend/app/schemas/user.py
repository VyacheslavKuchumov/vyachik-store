# app/schemas/user.py
from pydantic import BaseModel, EmailStr

# Базовая схема с общими полями, которые есть всегда
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Схема для СОЗДАНИЯ пользователя (Input DTO)
class UserCreate(UserBase):
    password: str # Клиент шлет сырой пароль, мы его валидируем здесь

# Схема для ОТВЕТА (Output DTO)
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    
    class Config:
        from_attributes = True