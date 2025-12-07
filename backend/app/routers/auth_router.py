# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db # Импортируем наш асинхронный генератор
from app.models.user_model import User
from app.models.auth_model import Auth
from app.schemas.user_schema import UserResponse, UserSignup
from app.schemas.auth_schema import TokenResponse
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_controller = AuthController()
user_controller = UserController()

# Эндпоинт для регистрации пользователя
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserSignup, db: AsyncSession = Depends(get_db)):
    # Проверяем, есть ли пользователь с таким email
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует."
        )
    
    # Хэшируем пароль
    password_hash = user_controller.get_password_hash(user.password)
    
    # Создаем нового пользователя
    db_user = User(email=user.email, username=user.username, password_hash=password_hash)
    
    # Добавляем в сессию (здесь await не нужен, это операция в памяти)
    db.add(db_user)

    # Фиксируем изменения в базе данных
    await db.commit()
    # Обновляем объект данными из базы (например, получаем присвоенный ID)
    await db.refresh(db_user)
    
    return db_user

# Эндпоинт для авторизации пользователя
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    response_model=TokenResponse
    ):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    
    if not user or not user_controller.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем JWT токен через AuthController
    access_token = auth_controller.create_access_token(data={"sub": user.username})
    refresh_token = auth_controller.create_refresh_token(data={"sub": user.username})
    
    # Здесь должна быть логика создания и возврата JWT токена
    return {"access_token": access_token, "token_type": "bearer"}
