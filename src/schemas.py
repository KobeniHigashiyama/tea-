from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# -------- Пользователи (Users) -------- #

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Пароль при создании нового пользователя

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True  # Позволяет использовать ORM объекты напрямую


# -------- Токены для аутентификации (Tokens) -------- #

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None


# -------- Чай (Tea) -------- #

class TeaBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    type: str
    weight: float
    in_stock: bool = True

class TeaCreate(TeaBase):
    pass  # Используем все поля из базовой схемы

class Tea(TeaBase):
    id: int

    class Config:
        orm_mode = True


# -------- Позиции заказа (Order Items) -------- #

class OrderItemBase(BaseModel):
    tea_id: int  # ID товара (чая)
    quantity: int  # Количество товара в заказе

class OrderItemCreate(OrderItemBase):
    pass  # Используем все поля из базовой схемы

class OrderItem(OrderItemBase):
    id: int
    tea: Optional[Tea]  # Вложенная схема чая для отображения информации о товаре

    class Config:
        orm_mode = True


# -------- Заказы (Orders) -------- #

class OrderBase(BaseModel):
    status: Optional[str] = "pending"  # Статус заказа (по умолчанию "в ожидании")

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]  # Список товаров (позиций) в заказе

class Order(OrderBase):
    id: int
    user_id: int  # ID пользователя, связанного с заказом
    created_at: datetime  # Время создания заказа
    items: List[OrderItem]  # Список позиций заказа (вложенные схемы)

    class Config:
        orm_mode = True  # ORM-режим для взаимодействия с моделями
