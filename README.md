# order-calculator

Сервис расчёта стоимости заказа интернет-магазина: сумма товаров, скидка за объём,
промокоды и доставка.

Проект вырос из одного скрипта `main.py` (см. первый коммит) в монорепозиторий:
доменная логика выделена в переиспользуемый пакет, вокруг него — HTTP API,
тесты, документация и контейнерное окружение.

## Что считает

| Правило | Значение |
|---|---|
| Скидка за объём | 5% от суммы товаров, если в заказе от 10 единиц |
| Промокоды | процентные или фиксированные, с минимальной суммой заказа (`STUDENT10`, `WELCOME200`, `BIGORDER15`) |
| Доставка | 300 ₽, бесплатно при сумме после скидок от 3000 ₽ |

Подробно — [docs/domain.md](docs/domain.md) и [docs/specification.md](docs/specification.md).

## Структура

```
.
├── packages/core/        # order-core — переиспользуемый пакет с доменной логикой (только stdlib)
├── app/api/              # order-api — HTTP API на FastAPI, использует order-core
│   └── Dockerfile        #   образ приложения (ядро собирается отдельной стадией)
├── tests/
│   ├── core/             #   unit-тесты доменной логики
│   ├── api/              #   тесты HTTP API (без базы)
│   ├── integration/      #   тесты с настоящим PostgreSQL
│   └── fixtures/         #   примеры заказов
├── docs/                 # документация Sphinx: домен, спецификация, архитектура, API
│   └── diagrams/         #   диаграммы Mermaid: контекст, use case, sequence
├── infra/
│   ├── compose.yaml      #   API + PostgreSQL
│   └── db/init.sql       #   схема и начальные промокоды
├── Makefile              # все команды проекта: make help
├── .python-version       # версия Python (3.10)
└── *.in / *.lock         # прямые зависимости / зафиксированное окружение
```

## Требования

- Python 3.10 (`.python-version`), GNU Make;
- Docker с Compose v2 — для `make up` и `make test-integration`.

## Быстрый старт

```bash
make install     # .venv + зависимости из lock-файлов + пакеты проекта
make check       # стиль, типы, тесты
make run         # API на http://localhost:8000 (промокоды в памяти)
```

Или в контейнерах вместе с PostgreSQL:

```bash
make up          # http://localhost:8000/docs
make down
```

Проверка запроса:

```bash
curl -X POST http://localhost:8000/quote \
  -H "Content-Type: application/json" \
  -d '{"items": [{"sku": "coffee", "price": 150, "quantity": 2}], "promo_code": "STUDENT10"}'
# {"subtotal":"300.00","discount":"30.00","delivery":"300.00","total":"570.00"}
```

## Команды

| Команда | Что делает |
|---|---|
| `make help` | список команд |
| `make install` | создать `.venv`, поставить зависимости и пакеты проекта |
| `make run` | запустить API локально |
| `make test` | тесты без базы данных |
| `make test-integration` | поднять PostgreSQL в контейнере и прогнать интеграционные тесты |
| `make coverage` | тесты с отчётом о покрытии (`htmlcov/index.html`) |
| `make lint` / `make format` | проверить / отформатировать код (ruff) |
| `make typecheck` | проверка типов (mypy) |
| `make check` | lint + typecheck + test |
| `make build-core` | собрать пакет `order-core` в `dist/` — без запуска приложения |
| `make docs` | собрать документацию в `docs/_build/html` |
| `make up` / `make down` / `make logs` | контейнерное окружение API + PostgreSQL |
| `make lock` | пересобрать lock-файлы после изменения `*.in` |
| `make clean` | удалить окружение, кэши и артефакты |

## Конфигурация

| Переменная | Где | Назначение |
|---|---|---|
| `DATABASE_URL` | API | строка подключения к PostgreSQL; если не задана — встроенные промокоды в памяти |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `API_PORT`, `DB_PORT` | `infra/.env` | настройки compose; пример — `infra/.env.example` |

## Использование ядра отдельно

```python
from decimal import Decimal
from order_core import Order, OrderItem, calculate_receipt

receipt = calculate_receipt(
    Order([OrderItem("coffee", Decimal("150"), 2)], "STUDENT10")
)
print(receipt.total)  # 570.00
```

## Документация

- [Предметная область](docs/domain.md)
- [Спецификация](docs/specification.md) — пронумерованные требования со ссылками на тесты
- [Архитектура](docs/architecture.md) — компоненты, границы, диаграммы
- [Руководство разработчика](docs/development.md) — ветки, коммиты, Pull Request

Полная собранная документация с API-справочником: `make docs`.
