# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import user_router
from app.database import Base, engine
from fastapi.responses import RedirectResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Vyachik's Store Backend", lifespan=lifespan)

# Регистрируем роутеры
app.include_router(user_router.router)


@app.get("/")
def root():
    # Редирект на документацию по API
    return RedirectResponse(url="/docs", status_code=307)
