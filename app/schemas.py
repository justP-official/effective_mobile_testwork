from datetime import datetime

from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, ValidationError

from .utils import StatusEnum


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=64, description='Название товара')
    description: str | None = Field(max_length=256, description='Описание товара')
    price: Decimal = Field(..., ge=0, decimal_places=2, description='Цена товара')
    quantity: int = Field(..., ge=0, description='Количество товара на складе')


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    order_id: int
    quantity: int = Field(..., gt=0, description='Количество товара в заказе')


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int


    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    creation_datetime: datetime = Field(..., description='Дата создания заказа')
    status: StatusEnum = Field(..., description='Статус заказа')

    @field_validator('creation_datetime')
    @classmethod
    def validate_creation_datetime(cls, value: datetime):
        if value and value.timestamp() > datetime.now().timestamp():
            raise ValidationError('Неверная дата')

        return value


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = Field(..., description='Элемент заказа')

class OrderUpdateStatus(BaseModel):
    status: StatusEnum = Field(..., description='Статус заказа')


class Order(OrderBase):
    id: int
    items: list[OrderItem] = Field(..., description='Элемент заказа')


    class Config:
        orm_mode = True
