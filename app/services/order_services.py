from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy.orm import Session
from .. import models, schemas

from .product_services import get_product

from ..utils import StatusEnum

def create_order_item(db: Session, order_item: schemas.OrderItemCreate) -> models.OrderItem:
    """
    Создает новый элемент заказа в базе данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param order_item: Данные для создания элемента заказа.
    :type order_item: schemas.OrderItemCreate
    :return: Созданный элемент заказа.
    :rtype: models.OrderItem
    """
    db_order_item = models.OrderItem(**order_item.model_dump())

    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)

    return db_order_item

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """
    Создает новый заказ в базе данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param order: Данные для создания заказа.
    :type order: schemas.OrderCreate
    :return: Созданный заказ.
    :rtype: models.Order
    :raises HTTPException: Если товара недостаточно на складе.
    """
    db_order = models.Order(creation_datetime=datetime.now(), status=order.status)

    for order_item in order.items:
        product = get_product(db, order_item.product_id)

        if product and product.quantity >= order_item.quantity:
            product.quantity -= order_item.quantity

            db_order_item = create_order_item(db, order_item)

            db.add(db_order_item)
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, 'Недостаточно товара на складе')
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> list[models.Order]:
    """
    Получает список заказов из базы данных с пагинацией.

    :param db: Сессия базы данных.
    :type db: Session
    :param skip: Количество заказов, которые нужно пропустить (по умолчанию 0).
    :type skip: int
    :param limit: Максимальное количество заказов для получения (по умолчанию 100).
    :type limit: int
    :return: Список заказов.
    :rtype: List[models.Order]
    """
    return db.query(models.Order).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int) -> models.Order:
    """
    Получает заказ по его идентификатору из базы данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param order_id: Идентификатор заказа.
    :type order_id: int
    :return: Заказ с указанным идентификатором или None, если заказ не найден.
    :rtype: models.Order
    """
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, order: schemas.OrderUpdateStatus, status: StatusEnum) -> models.Order:
    """
    Обновляет статус заказа в базе данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param order_id: Идентификатор заказа.
    :type order_id: int
    :param order: Данные для обновления статуса заказа.
    :type order: schemas.OrderUpdateStatus
    :param status: Новый статус заказа.
    :type status: StatusEnum
    :return: Обновленный заказ или None, если заказ не найден.
    :rtype: models.Order
    """
    db_order = get_order(db, order_id)

    if db_order:
        db_order.status = status

        db.commit()
        db.refresh(db_order)

    return db_order
