from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.databases import get_db
from src.schemas import Tea, TeaCreate
from src.routers.users import get_current_admin
from src.admin import crud
from fastapi.templating import Jinja2Templates
router = APIRouter()


templates = Jinja2Templates(directory="src/templates")





# Административный маршрут для создания товара
@router.post("/", response_model=Tea)
async def admin_create_tea(tea: TeaCreate, db: AsyncSession = Depends(get_db), current_admin: Tea = Depends(get_current_admin)):
    return await crud.create_tea(db=db, tea=tea)

# Административный маршрут для обновления товара
@router.put("/{tea_id}", response_model=Tea)
async def admin_update_tea(tea_id: int, tea: TeaCreate, db: AsyncSession = Depends(get_db), current_admin: Tea = Depends(get_current_admin)):
    db_tea = await crud.update_tea(db=db, tea_id=tea_id, tea=tea)
    if db_tea is None:
        raise HTTPException(status_code=404, detail="Tea not found")
    return db_tea

# Административный маршрут для удаления товара
@router.delete("/{tea_id}", response_model=Tea)
async def admin_delete_tea(tea_id: int, db: AsyncSession = Depends(get_db), current_admin: Tea = Depends(get_current_admin)):
    db_tea = await crud.delete_tea(db=db, tea_id=tea_id)
    if db_tea is None:
        raise HTTPException(status_code=404, detail="Tea not found")
    return db_tea



 #Страница для управления товарами (чай)
@router.get("/", response_class=HTMLResponse)
async def admin_tea_page(request: Request, db: AsyncSession = Depends(get_db), current_admin = Depends(get_current_admin)):
    teas = await crud.get_teas(db)
    return templates.TemplateResponse("admin/tea.html", {"request": request, "teas": teas})