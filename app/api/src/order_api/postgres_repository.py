"""Промокоды в PostgreSQL. Схема и начальные данные — infra/db/init.sql."""

from decimal import Decimal

import psycopg

from order_core import DiscountKind, PromoCode

SELECT_ALL = "SELECT code, kind, value, min_subtotal FROM promo_codes ORDER BY code"


class PostgresPromoCodeRepository:
    """Читает действующие промокоды из таблицы ``promo_codes``."""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def all(self) -> dict[str, PromoCode]:
        with psycopg.connect(self._dsn) as conn:
            rows = conn.execute(SELECT_ALL).fetchall()
        return {
            code: PromoCode(code, DiscountKind(kind), Decimal(value), Decimal(minimum))
            for code, kind, value, minimum in rows
        }
