from decimal import Decimal

import pytest

from order_core.errors import InvalidItemError
from order_core.models import OrderItem, money


def test_item_amount_is_price_times_quantity():
    assert OrderItem("coffee", Decimal("150.50"), 2).amount == Decimal("301.00")


def test_free_item_is_allowed():
    assert OrderItem("gift", Decimal("0"), 1).amount == 0


@pytest.mark.parametrize("quantity", [0, -1])
def test_non_positive_quantity_is_rejected(quantity):
    with pytest.raises(InvalidItemError, match="bad quantity"):
        OrderItem("coffee", Decimal("150"), quantity)


def test_negative_price_is_rejected():
    with pytest.raises(InvalidItemError, match="negative price"):
        OrderItem("coffee", Decimal("-0.01"), 1)


def test_money_rounds_half_up_to_cents():
    assert money(Decimal("10.004")) == Decimal("10.00")
    assert money(Decimal("10.005")) == Decimal("10.01")
