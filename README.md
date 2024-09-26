# Тестовое задание на позицию Junior Python developer в компанию Effective Mobile

## Задание: Разработка API для управления складом

[Задание (Google Docs)](https://docs.google.com/document/d/12y_vpjU_Uv70Tu0F4RPn8Af5Z20hyBo4IRNtSGm_tTg/edit?usp=sharing)

_Стек:_
- python 3.11;
- FastAPI;
- SQLAlchemy;
- pydantic;
- БД: SQLite;

---

## Как запустить проект

Клонируйте репозиторий

```
git clone https://github.com/justP-official/effective_mobile_testwork.git
```

### Без Docker

Создайте виртуальное окружение

```
python -m venv venv
```

Установите зависимости

```
pip install -r requirements.txt
```

Запустите тесты

```
pytest
```

Запустите сервер

```
uvicorn app.main:app
```

Документация будет доступна по адресу http://127.0.0.1:8000/docs

### С Docker

Соберите и запустите Docker-контейнеры:

```
docker-compose up --build
```

Документация будет доступна по адресу http://localhost:8000/docs

Запустите тесты:

```
docker-compose exec web pytest app/tests/
```

---

## Что можно улучшить:
- Заменить БД - для тестого задания подойдёт и SQLite, но для реального проекта лучше выбрать PostgreSQL/MySQL;
- Сделать код асинхронным - SQLite не поддерживает асинхронные операции, если сменить БД, то можно добавить асинхронности;
- ~~Тесты~~ Готово;
- ~~Контейнеризация~~ Готово;
