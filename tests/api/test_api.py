"""Тесты HTTP API. Сценарии повторяют smoke-тесты исходного скрипта."""

import json
from decimal import Decimal
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from order_api.main import create_app
from order_api.promo_repository import InMemoryPromoCodeRepository
from order_core import DiscountKind, PromoCode

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def load(fixture: str) -> dict:
    return json.loads((FIXTURES / fixture).read_text(encoding="utf-8"))


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


@pytest.mark.parametrize(
    "fixture, expected",
    [
        ("student10.json", ["570.00", "57.00", "300.00", "813.00"]),
        ("volume_free_delivery.json", ["4000.00", "200.00", "0.00", "3800.00"]),
        ("welcome200.json", ["1200.00", "200.00", "300.00", "1300.00"]),
    ],
)
def test_quote_returns_receipt(client, fixture, expected):
    response = client.post("/quote", json=load(fixture))
    assert response.status_code == 200
    body = response.json()
    assert [body["subtotal"], body["discount"], body["delivery"], body["total"]] == (
        expected
    )


@pytest.mark.parametrize(
    "fixture, error",
    [
        ("empty.json", "EmptyOrderError"),
        ("zero_quantity.json", "InvalidItemError"),
        ("negative_price.json", "InvalidItemError"),
        ("unknown_code.json", "UnknownPromoCodeError"),
        ("welcome200_too_small.json", "PromoCodeNotApplicableError"),
    ],
)
def test_domain_errors_return_422_with_error_type(client, fixture, error):
    response = client.post("/quote", json=load(fixture))
    assert response.status_code == 422
    assert response.json()["error"] == error


def test_malformed_request_is_rejected_by_validation(client):
    response = client.post("/quote", json={"items": [{"sku": "coffee"}]})
    assert response.status_code == 422


def test_promo_codes_come_from_repository():
    repository = InMemoryPromoCodeRepository(
        {"HALF": PromoCode("HALF", DiscountKind.PERCENT, Decimal("50"))}
    )
    client = TestClient(create_app(repository))

    assert [p["code"] for p in client.get("/promo-codes").json()] == ["HALF"]
    order = {
        "items": [{"sku": "tea", "price": 1000, "quantity": 1}],
        "promo_code": "HALF",
    }
    assert client.post("/quote", json=order).json()["discount"] == "500.00"
    order["promo_code"] = "STUDENT10"
    assert client.post("/quote", json=order).status_code == 422
