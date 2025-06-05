# ============================
# backend/Makefile
# ============================
.PHONY: help install test lint format run migrate

help:
	@echo "Available commands:"
	@echo "  install    Install dependencies"
	@echo "  test       Run tests"
	@echo "  lint       Run linting"
	@echo "  format     Format code"
	@echo "  run        Run development server"
	@echo "  migrate    Run database migrations"
	@echo "  celery     Run Celery worker"
	@echo "  flower     Run Flower (Celery monitoring)"

install:
	pip install -r requirements.txt

test:
	pytest

test-cov:
	pytest --cov=app --cov-report=html

lint:
	flake8 app tests
	mypy app

format:
	black app tests
	isort app tests

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(message)"

celery:
	celery -A app.core.celery_app worker -l info

celery-beat:
	celery -A app.core.celery_app beat -l info

flower:
	celery -A app.core.celery_app flower