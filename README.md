# Codemath Solver API 🧮

A modular FastAPI backend for managing math problems, solutions, and explanations, following clean architecture principles. Built with FastAPI, SQLAlchemy, Pydantic, and PostgreSQL.

## ✨ Features

- 📝 CRUD APIs for Problems, Solutions, Explanations, Tags
- 🏗️ Clean architecture: models, CRUD, service, and API layers
- 📦 Unified API response schema for all endpoints
- 🗄️ SQLAlchemy ORM models and Alembic migrations
- 📄 Pydantic schemas for input/output/serialization
- 🧠 Business logic in service layer
- 🚦 Consistent error handling for DB constraints and not found
- 🧪 Unit tests with FastAPI TestClient
- 🎨 Code style: Black, Flake8, pre-commit hooks
- 🐳 Docker and docker-compose support

## 🗂️ Project Structure

```
app/
  api/v1/endpoints/   # API routers
  db/models/          # SQLAlchemy models
  db/crud/            # CRUD classes
  schemas/            # Pydantic schemas
  services/           # Business logic
  db/session.py       # DB session
  main.py             # FastAPI app
alembic/              # DB migrations
requirements.txt      # Python dependencies
Dockerfile            # Docker image
```

## 🚀 Quick Start

1. **Clone the repo:**
   ```sh
   git clone <repo-url>
   cd codemath-solver-api
   ```
2. **Configure environment:**
   - Copy `.env.example` to `.env` and set DB credentials
3. **Run with Docker:**
   ```sh
   docker-compose up --build
   ```
4. **Run migrations:**
   ```sh
   docker-compose exec backend alembic upgrade head
   ```
5. **API Docs:**
   - Visit [http://localhost:8000/docs](http://localhost:8000/docs) 📚

## 🧪 Testing

```sh
pytest
```

## 📤 API Response Format

All endpoints return:

```json
{
  "status_code": 200,
  "data": {...},
  "message": "Success"
}
```

## 📄 License

MIT
