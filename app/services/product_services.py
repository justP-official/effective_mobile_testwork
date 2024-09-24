from sqlalchemy.orm import Session
from .. import models, schemas


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """
    Создает новый продукт в базе данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param product: Данные для создания продукта.
    :type product: schemas.ProductCreate
    :return: Созданный продукт.
    :rtype: models.Product
    """
    db_product = models.Product(**product.model_dump())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 100) -> list[models.Product]:
    """
    Получает список продуктов из базы данных с пагинацией.

    :param db: Сессия базы данных.
    :type db: Session
    :param skip: Количество продуктов, которые нужно пропустить (по умолчанию 0).
    :type skip: int
    :param limit: Максимальное количество продуктов для получения (по умолчанию 100).
    :type limit: int
    :return: Список продуктов.
    :rtype: List[models.Product]
    """
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int) -> models.Product:
    """
    Получает продукт по его идентификатору из базы данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param product_id: Идентификатор продукта.
    :type product_id: int
    :return: Продукт с указанным идентификатором или None, если продукт не найден.
    :rtype: models.Product
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductCreate) -> models.Product:
    """
    Обновляет информацию о продукте в базе данных.

    :param db: Сессия базы данных.
    :type db: Session
    :param product_id: Идентификатор продукта.
    :type product_id: int
    :param product: Данные для обновления продукта.
    :type product: schemas.ProductCreate
    :return: Обновленный продукт или None, если продукт не найден.
    :rtype: models.Product
    """
    db_product = get_product(db, product_id)

    if db_product:
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        
        db.commit()
        db.refresh(db_product)

    return db_product

def delete_product(db: Session, product_id: int) -> dict[str, str] | None:
    """
    Удаляет продукт из базы данных по его идентификатору.

    :param db: Сессия базы данных.
    :type db: Session
    :param product_id: Идентификатор продукта.
    :type product_id: int
    :return: Сообщение об успешном удалении или None, если продукт не найден.
    :rtype: dict[str, str] | None
    """
    db_product = get_product(db, product_id)

    if db_product:
        db.delete(db_product)
        db.commit()

        return {'Message': 'Продукт успешно удалён'}
    