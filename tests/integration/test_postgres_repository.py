"""Интеграционные тесты с настоящим PostgreSQL.

Запускаются только при заданном ``DATABASE_URL`` (``make test-integration``
поднимает тестовую базу в контейнере). Без него — пропускаются.
"""

import os
from decimal import Decimal

import pytest

from order_core import DiscountKind, Order, OrderItem, calculate_receipt

DATABASE_URL = os.getenv("DATABASE_URL")

pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="DATABASE_URL is not set")


@pytest.fixture
def repository():
    from order_api.postgres_repository import PostgresPromoCodeRepository

    assert DATABASE_URL is not None
    return PostgresPromoCodeRepository(DATABASE_URL)


def test_seeded_promo_codes_are_loaded(repository):
    codes = repository.all()
    assert {"STUDENT10", "WELCOME200", "BIGORDER15"} <= codes.keys()
    welcome = codes["WELCOME200"]
    assert welcome.kind is DiscountKind.FIXED
    assert welcome.value == Decimal("200")
    assert welcome.min_subtotal == Decimal("1000")


def test_promo_code_from_database_is_applied(repository):
    order = Order([OrderItem("tea", Decimal("5000"), 1)], "BIGORDER15")
    receipt = calculate_receipt(order, repository.all())
    assert receipt.discount == Decimal("750.00")
