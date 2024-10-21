from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base

# Модель для товаров (Чай)
class Tea(Base):
    __tablename__ = "tea"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

    orders = relationship("OrderItem", back_populates="tea")

# Модель для пользователей
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="user")

# Модель для заказов
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

# Модель для позиций заказа
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    tea_id = Column(Integer, ForeignKey("tea.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    tea = relationship("Tea", back_populates="orders")
