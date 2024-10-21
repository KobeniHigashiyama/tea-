from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud, schemas
from src.databases import get_db
from src.routers.users import get_current_user

router = APIRouter()

# Получение списка всех заказов для текущего пользователя
@router.get("/", response_model=list[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    orders = await crud.get_orders_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return orders

# Получение одного заказа по ID
@router.get("/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    order = await crud.get_order(db=db, order_id=order_id)
    if order is None or order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return order

# Создание нового заказа
@router.post("/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return await crud.create_order(db=db, order=order, user_id=current_user.id)

# Обновление существующего заказа
@router.put("/{order_id}", response_model=schemas.Order)
async def update_order(order_id: int, order: schemas.OrderCreate, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_order = await crud.get_order(db=db, order_id=order_id)
    if db_order is None or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return await crud.update_order(db=db, order_id=order_id, order=order)

# Удаление заказа
@router.delete("/{order_id}", response_model=schemas.Order)
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_order = await crud.get_order(db=db, order_id=order_id)
    if db_order is None or db_order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return await crud.delete_order(db=db, order_id=order_id)
