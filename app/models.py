from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

from .utils import StatusEnum


class Product(Base):
    '''Модель БД для описания продукта'''
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


class Order(Base):
    '''Модель БД для описания заказа'''
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    creation_datetime = Column(DateTime)
    status = Column(Enum(StatusEnum))

    items = relationship('OrderItem', back_populates='order')


class OrderItem(Base):
    '''Модель БД для описания элемента заказа'''
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement="auto", index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship('Order', back_populates='items')
    product = relationship('Product')
