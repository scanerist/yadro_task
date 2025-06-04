## Требования

- Python 3.11+
- PostgreSQL
- pip 
- Docker 




## 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта и заполните его, например:

```
DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/shortener
JWT_SECRET=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXP_MINUTES=60
```

## 2. Установка зависимостей

### Через pip

```bash
python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Настройка базы данных

### Через Docker 

```bash
docker-compose up -d
```

## 4. Применение миграций

```bash
alembic init -t async migraition 

alembic upgrade head
```

## 5. Запуск приложения

```bash
 uvicorn main:app --host localhost --port 8000 --reload 
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

## 6. Документация API

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Примеры запросов

- Регистрация: `POST /api/auth/register`
- Логин: `POST /api/auth/login`
- Создание ссылки: `POST /api/links/create`
- Перенаправление: `GET /{short_code}`
