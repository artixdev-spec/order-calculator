"""Smoke-тесты исходного скрипта main.py.

Фиксируют наблюдаемое поведение до рефакторинга: какой заказ даёт какой чек
и на каких данных скрипт завершается с ошибкой.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).parent / "fixtures"


def run_main(fixture: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "main.py"), str(FIXTURES / fixture)],
        capture_output=True,
        text=True,
    )


def receipt(subtotal: str, discount: str, delivery: str, total: str) -> str:
    return (
        f"subtotal: {subtotal}\ndiscount: {discount}\n"
        f"delivery: {delivery}\ntotal: {total}\n"
    )


@pytest.mark.parametrize(
    "fixture, expected",
    [
        ("student10.json", receipt("570.00", "57.00", "300.00", "813.00")),
        (
            "volume_free_delivery.json",
            receipt("4000.00", "200.00", "0.00", "3800.00"),
        ),
        ("welcome200.json", receipt("1200.00", "200.00", "300.00", "1300.00")),
    ],
)
def test_valid_order_prints_receipt(fixture, expected):
    result = run_main(fixture)
    assert result.returncode == 0
    assert result.stdout == expected


@pytest.mark.parametrize(
    "fixture, message",
    [
        ("empty.json", "order is empty"),
        ("zero_quantity.json", "bad quantity"),
        ("negative_price.json", "negative price"),
        ("unknown_code.json", "unknown promo code"),
        ("welcome200_too_small.json", "needs order from 1000"),
    ],
)
def test_invalid_order_fails_with_message(fixture, message):
    result = run_main(fixture)
    assert result.returncode == 1
    assert message in result.stdout
