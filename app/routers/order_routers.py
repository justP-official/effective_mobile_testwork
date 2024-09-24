from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services import order_services

from ..utils import StatusEnum

router = APIRouter(prefix='/orders')

@router.post('/')
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)) -> schemas.Order:
    """
    Создает новый заказ.

    :param order: Данные для создания заказа.
    :type order: schemas.OrderCreate
    :param db: Сессия базы данных.
    :type db: Session
    :return: Созданный заказ.
    :rtype: schemas.Order
    """
    return order_services.create_order(db, order)

@router.get('/')
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.Order]:
    """
    Получает список заказов с пагинацией.

    :param skip: Количество заказов, которые нужно пропустить (по умолчанию 0).
    :type skip: int
    :param limit: Максимальное количество заказов для получения (по умолчанию 100).
    :type limit: int
    :param db: Сессия базы данных.
    :type db: Session
    :return: Список заказов.
    :rtype: list[schemas.Order]
    """
    return order_services.get_orders(db, skip, limit)

@router.get('/{order_id}')
def get_order(order_id: int, db: Session = Depends(get_db)) -> schemas.Order:
    """
    Получает заказ по его идентификатору.

    :param order_id: Идентификатор заказа.
    :type order_id: int
    :param db: Сессия базы данных.
    :type db: Session
    :return: Заказ с указанным идентификатором.
    :rtype: schemas.Order
    :raises HTTPException: Если заказ не найден.
    """
    order = order_services.get_order(db, order_id)

    if order is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Заказ не найден')
    
    return order

@router.patch('/{order_id}/status')
def update_order_status(order_id: int, 
                        order: schemas.OrderUpdateStatus, 
                        status: StatusEnum, 
                        db: Session = Depends(get_db)
                        ) -> schemas.Order:
    """
    Обновляет статус заказа.

    :param order_id: Идентификатор заказа.
    :type order_id: int
    :param order: Данные для обновления статуса заказа.
    :type order: schemas.OrderUpdateStatus
    :param status: Новый статус заказа.
    :type status: StatusEnum
    :param db: Сессия базы данных.
    :type db: Session
    :return: Обновленный заказ.
    :rtype: schemas.Order
    """
    return order_services.update_order_status(db, order_id, order, status)
