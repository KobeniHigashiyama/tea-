from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud, schemas
from src.databases import AsyncSessionLocal

router = APIRouter()

# Асинхронная зависимость для получения сессии базы данных
async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Асинхронное получение списка всех чаев
@router.get("/", response_model=list[schemas.Tea])
async def read_teas(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    teas = await crud.get_teas(db, skip=skip, limit=limit)
    return teas

# Асинхронное получение одного чая по ID
@router.get("/{tea_id}", response_model=schemas.Tea)
async def read_tea(tea_id: int, db: AsyncSession = Depends(get_db)):
    tea = await crud.get_tea(db, tea_id=tea_id)
    if tea is None:
        raise HTTPException(status_code=404, detail="Tea not found")
    return tea

# Асинхронное создание нового чая
@router.post("/", response_model=schemas.Tea)
async def create_tea(tea: schemas.TeaCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_tea(db=db, tea=tea)

# Асинхронное обновление чая
@router.put("/{tea_id}", response_model=schemas.Tea)
async def update_tea(tea_id: int, tea: schemas.TeaCreate, db: AsyncSession = Depends(get_db)):
    db_tea = await crud.get_tea(db, tea_id=tea_id)
    if db_tea is None:
        raise HTTPException(status_code=404, detail="Tea not found")
    return await crud.update_tea(db=db, tea_id=tea_id, tea=tea)

# Асинхронное удаление чая
@router.delete("/{tea_id}", response_model=schemas.Tea)
async def delete_tea(tea_id: int, db: AsyncSession = Depends(get_db)):
    db_tea = await crud.get_tea(db, tea_id=tea_id)
    if db_tea is None:
        raise HTTPException(status_code=404, detail="Tea not found")
    return await crud.delete_tea(db=db, tea_id=tea_id)
