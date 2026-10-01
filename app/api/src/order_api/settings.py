"""Конфигурация приложения из переменных окружения."""

import os

from order_api.promo_repository import InMemoryPromoCodeRepository, PromoCodeRepository


def promo_repository_from_env() -> PromoCodeRepository:
    """Выбрать хранилище промокодов.

    Если задан ``DATABASE_URL`` — PostgreSQL, иначе встроенные промокоды в памяти
    (локальный запуск и тесты без базы).
    """
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        return InMemoryPromoCodeRepository()
    from order_api.postgres_repository import PostgresPromoCodeRepository

    return PostgresPromoCodeRepository(dsn)
