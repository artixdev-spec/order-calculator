# Единая точка входа для команд проекта. `make help` — список целей.
# Требования: Python 3.10 (см. .python-version), GNU Make; для docker-целей — Docker.

PYTHON ?= python3
VENV   := .venv
BIN    := $(VENV)/bin
PY     := $(BIN)/python

.DEFAULT_GOAL := help
.PHONY: help venv install lock run test coverage lint format typecheck check build-core clean

help: ## показать список команд
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

$(PY):
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --upgrade pip

venv: $(PY) ## создать виртуальное окружение .venv

install: $(PY) ## установить зависимости из lock-файлов и пакеты проекта
	$(PY) -m pip install -r app/api/requirements.lock -r requirements-dev.lock
	$(PY) -m pip install --no-deps -e packages/core -e app/api

lock: $(PY) ## пересобрать lock-файлы из *.in
	$(PY) -m pip install uv
	$(BIN)/uv pip compile --python-version 3.10 app/api/requirements.in -o app/api/requirements.lock
	$(BIN)/uv pip compile --python-version 3.10 requirements-dev.in -o requirements-dev.lock

run: ## запустить API локально на http://localhost:8000
	$(BIN)/uvicorn order_api.main:app --reload --port 8000

test: ## запустить тесты
	$(PY) -m pytest

coverage: ## тесты с отчётом о покрытии (терминал + htmlcov/)
	$(PY) -m pytest --cov --cov-report=term-missing --cov-report=html

lint: ## проверить стиль (ruff)
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .

format: ## отформатировать код (ruff)
	$(BIN)/ruff check --fix .
	$(BIN)/ruff format .

typecheck: ## проверить типы (mypy)
	$(BIN)/mypy packages/core/src app/api/src

check: lint typecheck test ## все проверки: стиль, типы, тесты

build-core: ## собрать пакет order-core в dist/ (без запуска приложения)
	$(PY) -m build packages/core --outdir dist

clean: ## удалить окружение, кэши и артефакты сборки
	rm -rf $(VENV) dist htmlcov .coverage .pytest_cache .mypy_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -name '*.egg-info' -type d -prune -exec rm -rf {} +
