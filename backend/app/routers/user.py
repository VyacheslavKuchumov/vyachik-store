# app/routers/user.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db # Импортируем наш асинхронный генератор
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    # FastAPI сам вызовет get_db, дождется сессии и передаст её сюда
    db: AsyncSession = Depends(get_db) 
):
    # Хешируем пароль (в реальном проекте используйте Bcrypt!)
    fake_hashed_password = f"secret_hash_{user.password}" 

    db_user = User(email=user.email, username=user.username, hashed_password=fake_hashed_password)
    
    # Добавляем в сессию (здесь await не нужен, это операция в памяти)
    db.add(db_user)
    
    # А вот здесь мы "отпускаем" управление, пока база сохраняет данные.
    # В это время сервер может обрабатывать запросы других пользователей!
    await db.commit()
    
    # Обновляем объект данными из базы (например, получаем присвоенный ID)
    await db.refresh(db_user)
    
    return db_user

# получить пользователя по ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.get(User, user_id)
    return result


# получить всех пользователей
@router.get("/", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

