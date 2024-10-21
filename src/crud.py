from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import models, schemas
from src.auth import hash_password,verify_password

# -------- Чай (Tea) -------- #

#  получение списка всех чаев
async def get_teas(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Tea).offset(skip).limit(limit))
    return result.scalars().all()

# получение одного чая по ID
async def get_tea(db: AsyncSession, tea_id: int):
    result = await db.execute(select(models.Tea).filter(models.Tea.id == tea_id))
    return result.scalar()

#  создание нового чая
async def create_tea(db: AsyncSession, tea: schemas.TeaCreate):
    db_tea = models.Tea(**tea.dict())
    db.add(db_tea)
    await db.commit()
    await db.refresh(db_tea)
    return db_tea

# Аобновление чая
async def update_tea(db: AsyncSession, tea_id: int, tea: schemas.TeaCreate):
    result = await db.execute(select(models.Tea).filter(models.Tea.id == tea_id))
    db_tea = result.scalar()
    if db_tea:
        for key, value in tea.dict().items():
            setattr(db_tea, key, value)
        await db.commit()
        await db.refresh(db_tea)
    return db_tea

#  удаление чая
async def delete_tea(db: AsyncSession, tea_id: int):
    result = await db.execute(select(models.Tea).filter(models.Tea.id == tea_id))
    db_tea = result.scalar()
    if db_tea:
        await db.delete(db_tea)
        await db.commit()
    return db_tea


# -------- Пользователи (Users) -------- #

#  получение списка всех пользователей
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

#  получение одного пользователя по ID
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalar()

#  создание нового пользователя
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)  # Функция хеширования пароля
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
# Получение пользователя по email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalar()
# обновление пользователя
async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.hashed_password = hash_password(user.password)
        await db.commit()
        await db.refresh(db_user)
    return db_user

#  удаление пользователя
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    db_user = result.scalar()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user

# (заменить  на реальную реализацию)
def hash_password(password: str) -> str:
    return f"hashed_{password}"


# -------- Заказы (Orders) -------- #

#  получение всех заказов (для администраторов)
async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.scalars().all()

# получение всех заказов пользователя
async def get_orders_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Order).filter(models.Order.user_id == user_id).offset(skip).limit(limit))
    return result.scalars().all()

#  получение одного заказа по ID
async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    return result.scalar()

#  создание нового заказа
async def create_order(db: AsyncSession, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(user_id=user_id, status=order.status)
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    
    # Добавление товаров (позиций) в заказ
    for item in order.items:
        db_item = models.OrderItem(order_id=db_order.id, tea_id=item.tea_id, quantity=item.quantity)
        db.add(db_item)
    
    await db.commit()
    return db_order

#  обновление заказа
async def update_order(db: AsyncSession, order_id: int, order: schemas.OrderCreate):
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    db_order = result.scalar()
    if db_order:
        db_order.status = order.status
        await db.commit()
        await db.refresh(db_order)
    return db_order

# удаление заказа
async def delete_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(models.Order).filter(models.Order.id == order_id))
    db_order = result.scalar()
    if db_order:
        await db.delete(db_order)
        await db.commit()
    return db_order
