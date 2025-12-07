# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db # Импортируем наш асинхронный генератор
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController

router = APIRouter(prefix="/users", tags=["Users"])
user_controller = UserController()
auth_controller = AuthController()

# Эндпоинт для создания пользователя (админка)
@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    password_hash = user_controller.get_password_hash(user.password)
    db_user = User(email=user.email, username=user.username, password_hash=password_hash, is_superuser=user.is_superuser)
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

# Эндпоинт для получения пользователя по ID (админка)
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.get(User, user_id)
    return result


# Эндпоинт для получения всех пользователей (админка)
@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    username = Depends(user_controller.get_current_user)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

