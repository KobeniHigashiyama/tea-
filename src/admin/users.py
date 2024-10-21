from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.databases import get_db
from src.schemas import User, UserCreate
from src.routers.users import get_current_admin
from src.admin import crud
from fastapi.templating import Jinja2Templates

router = APIRouter()


templates = Jinja2Templates(directory="src/templates")
# Административный маршрут для получения списка всех пользователей
@router.get("/", response_model=list[User])
async def admin_get_users(db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    users = await crud.get_users(db=db)
    return users

# Административный маршрут для обновления данных пользователя (например, назначение администратора)
@router.put("/{user_id}", response_model=User)
async def admin_update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_user = await crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Административный маршрут для удаления пользователя
@router.delete("/{user_id}", response_model=User)
async def admin_delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    db_user = await crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




# Страница для управления пользователями
@router.get("/", response_class=HTMLResponse)
async def admin_users_page(request: Request, db: AsyncSession = Depends(get_db), current_admin = Depends(get_current_admin)):
    users = await crud.get_users(db)
    return templates.TemplateResponse("admin/users.html", {"request": request, "users": users})