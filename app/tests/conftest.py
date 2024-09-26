from datetime import datetime
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient
from ..main import app
from ..database import Base, get_db


SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def product_payload():
    return {
        "name": "Test product",
        "description": "Test description",
        "price": 12.34,
        "quantity": 100,
        "id": 1
    }

@pytest.fixture()
def product_update_payload():
    return {
        "name": "Test product updated",
        "description": "Test description",
        "price": 12.34,
        "quantity": 100,
        "id": 1
    }

@pytest.fixture()
def order_item_payload():
    return {
        "order_id": 1,
        "product_id": 1,
        "quantity": 1
    }

@pytest.fixture()
def order_payload():
    return {
        "creation_datetime": datetime.now().isoformat(),
        "status": "В процессе",
        "id": 1,

        "items": [
            {
                "order_id": 1,
                "product_id": 1,
                "quantity": 10
            }
        ]
    }

@pytest.fixture()
def order_update_status_payload():
    return {
        "status": "Отправлен"
    }
