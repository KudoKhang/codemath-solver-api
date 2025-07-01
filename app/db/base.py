from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here so Alembic can detect them
from app.db.models import explanation, problem, problem_tag, solution, tag  # noqa
