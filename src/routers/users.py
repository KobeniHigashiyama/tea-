from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from src import crud, schemas
from src.databases import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth import create_access_token, verify_password, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.schemas import User

router = APIRouter()

# Зависимость для проверки токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Асинхронное получение списка всех пользователей
@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users

# Асинхронное получение одного пользователя по ID
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Асинхронное создание нового пользователя
@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, user=user)

# Асинхронное обновление пользователя
@router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.update_user(db=db, user_id=user_id, user=user)

# Асинхронное удаление пользователя
@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.delete_user(db=db, user_id=user_id)



# Получение текущего пользователя на основе токена
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = await crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user


# Регистрация нового пользователя
@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)




# Вход в систему (аутентификация)
@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

# Получение данных о текущем пользователе
@router.get("/me", response_model=schemas.User)
async def read_current_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user

# Проверка, является ли пользователь администратором
async def get_current_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user