from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services import product_services

router = APIRouter(prefix='/products')

@router.post('/')
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)) -> schemas.Product:
    """
    Создает новый продукт.

    :param product: Данные для создания продукта.
    :type product: schemas.ProductCreate
    :param db: Сессия базы данных.
    :type db: Session
    :return: Созданный продукт.
    :rtype: schemas.Product
    """
    return product_services.create_product(db, product)

@router.get('/')
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.Product]:
    """
    Получает список продуктов с пагинацией.

    :param skip: Количество продуктов, которые нужно пропустить (по умолчанию 0).
    :type skip: int
    :param limit: Максимальное количество продуктов для получения (по умолчанию 100).
    :type limit: int
    :param db: Сессия базы данных.
    :type db: Session
    :return: Список продуктов.
    :rtype: list[schemas.Product]
    """
    return product_services.get_products(db, skip, limit)

@router.get('/{product_id}')
def get_product(product_id: int, db: Session = Depends(get_db)) -> schemas.Product:
    """
    Получает продукт по его идентификатору.

    :param product_id: Идентификатор продукта.
    :type product_id: int
    :param db: Сессия базы данных.
    :type db: Session
    :return: Продукт с указанным идентификатором.
    :rtype: schemas.Product
    :raises HTTPException: Если продукт не найден.
    """
    product = product_services.get_product(db, product_id)

    if product is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Продукт не найден')
    
    return product

@router.put('/{product_id}')
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)) -> schemas.Product:
    """
    Обновляет информацию о продукте.

    :param product_id: Идентификатор продукта.
    :type product_id: int
    :param product: Данные для обновления продукта.
    :type product: schemas.ProductCreate
    :param db: Сессия базы данных.
    :type db: Session
    :return: Обновленный продукт.
    :rtype: schemas.Product
    """
    return product_services.update_product(db, product_id, product)

@router.delete('/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)) -> dict[str, str] | None:
    """
    Удаляет продукт по его идентификатору.

    :param product_id: Идентификатор продукта.
    :type product_id: int
    :param db: Сессия базы данных.
    :type db: Session
    :return: Сообщение об успешном удалении или None, если продукт не найден.
    :rtype: dict[str, str] | None
    """
    return product_services.delete_product(db, product_id)
