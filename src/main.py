from fastapi import FastAPI
from src.routers import tea, users, orders
from src.databases import create_db_and_tables
from src.admin import users as admin_users, tea as admin_tea 
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv




app = FastAPI(
    title="Tea Shop API",
    description="API для управления магазином чаев",
    version="1.0.0"
)

#  из .env
load_dotenv()

# Доступ к переменным окружения
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")


app.include_router(tea.router, prefix="/tea", tags=["Tea"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

app.include_router(admin_users.router, prefix="/admin/users", tags=["Admin Users"])
app.include_router(admin_tea.router, prefix="/admin/tea", tags=["Admin Tea"])
# старт 
@app.on_event("startup")
async def on_startup():
   
    await create_db_and_tables()

# Пример корневого маршрута
@app.get("/")
async def read_root():
    return {"message": "Salam!"}

app.mount("/static", StaticFiles(directory="src/static"), name="static")