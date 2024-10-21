from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import models, schemas
from src.auth import hash_password

# -------- Пользователи (Admin Users) -------- #

# Получение всех пользователей
async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()

# Обновление пользователя (назначение администратора и т.д.)
async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = hash_password(user.password)
        db_user.is_admin = user.is_admin  # Возможность обновлять роль администратора
        await db.commit()
        await db.refresh(db_user)
    return db_user

# Удаление пользователя
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user

# -------- Товары (Admin Tea) -------- #

# Создание товара (чая)
async def create_tea(db: AsyncSession, tea: schemas.TeaCreate):
    db_tea = models.Tea(**tea.dict())
    db.add(db_tea)
    await db.commit()
    await db.refresh(db_tea)
    return db_tea

# Обновление товара
async def update_tea(db: AsyncSession, tea_id: int, tea: schemas.TeaCreate):
    result = await db.execute(select(models.Tea).filter(models.Tea.id == tea_id))
    db_tea = result.scalar()
    if db_tea:
        for key, value in tea.dict().items():
            setattr(db_tea, key, value)
        await db.commit()
        await db.refresh(db_tea)
    return db_tea

# Удаление товара
async def delete_tea(db: AsyncSession, tea_id: int):
    result = await db.execute(select(models.Tea).filter(models.Tea.id == tea_id))
    db_tea = result.scalar()
    if db_tea:
        await db.delete(db_tea)
        await db.commit()
    return db_tea
