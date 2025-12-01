# app/main.py
from fastapi import FastAPI
# Импортируем наш новый модуль с роутером
from app.routers import user
from app.database import Base, engine


app = FastAPI(title="My Architecture App")

# Подключаем роутер к главному приложению.
# Это похоже на подключение плагина.
app.include_router(user.router)

# Создаем все таблицы в базе данных при старте приложения
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "Приложение работает!"}