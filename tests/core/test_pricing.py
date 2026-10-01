from decimal import Decimal

import pytest

from order_core.errors import (
    EmptyOrderError,
    PromoCodeNotApplicableError,
    UnknownPromoCodeError,
)
from order_core.models import Order, OrderItem
from order_core.pricing import calculate_receipt
from order_core.promo import DiscountKind, PromoCode


def item(price: str, quantity: int = 1) -> OrderItem:
    return OrderItem("sku", Decimal(price), quantity)


def test_order_without_discounts_pays_delivery():
    receipt = calculate_receipt(Order([item("150", 2), item("90", 3)]))
    assert receipt.subtotal == Decimal("570.00")
    assert receipt.discount == Decimal("0.00")
    assert receipt.delivery == Decimal("300.00")
    assert receipt.total == Decimal("870.00")


def test_percent_promo_code_is_applied():
    receipt = calculate_receipt(Order([item("150", 2), item("90", 3)], "STUDENT10"))
    assert receipt.discount == Decimal("57.00")
    assert receipt.total == Decimal("813.00")


def test_volume_discount_starts_from_ten_units():
    assert calculate_receipt(Order([item("100", 9)])).discount == 0
    assert calculate_receipt(Order([item("100", 10)])).discount == Decimal("50.00")


def test_volume_discount_counts_units_across_items():
    receipt = calculate_receipt(Order([item("100", 4), item("100", 6)]))
    assert receipt.discount == Decimal("50.00")


def test_volume_and_promo_discounts_add_up():
    receipt = calculate_receipt(Order([item("100", 10)], "STUDENT10"))
    assert receipt.discount == Decimal("150.00")


def test_free_delivery_boundary_is_inclusive():
    assert calculate_receipt(Order([item("3000")])).delivery == 0
    assert calculate_receipt(Order([item("2999.99")])).delivery == Decimal("300.00")


def test_free_delivery_is_checked_after_discount():
    receipt = calculate_receipt(Order([item("3200")], "WELCOME200"))
    assert receipt.delivery == 0
    receipt = calculate_receipt(Order([item("3100")], "WELCOME200"))
    assert receipt.delivery == Decimal("300.00")


def test_discount_never_exceeds_subtotal():
    huge = {"HUGE": PromoCode("HUGE", DiscountKind.FIXED, Decimal("10000"))}
    receipt = calculate_receipt(Order([item("500")], "HUGE"), huge)
    assert receipt.discount == Decimal("500.00")
    assert receipt.total == Decimal("300.00")


def test_custom_promo_codes_replace_defaults():
    with pytest.raises(UnknownPromoCodeError):
        calculate_receipt(Order([item("500")], "STUDENT10"), promo_codes={})


def test_empty_order_is_rejected():
    with pytest.raises(EmptyOrderError):
        calculate_receipt(Order([]))


def test_unknown_promo_code_is_rejected():
    with pytest.raises(UnknownPromoCodeError):
        calculate_receipt(Order([item("500")], "FREE100"))


def test_not_applicable_promo_code_is_rejected():
    with pytest.raises(PromoCodeNotApplicableError):
        calculate_receipt(Order([item("300")], "WELCOME200"))


def test_empty_promo_code_is_ignored():
    assert calculate_receipt(Order([item("500")], "")).discount == 0
