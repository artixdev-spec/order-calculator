from decimal import Decimal

import pytest

from order_core.errors import PromoCodeNotApplicableError, UnknownPromoCodeError
from order_core.promo import (
    DEFAULT_PROMO_CODES,
    DiscountKind,
    PromoCode,
    find_promo_code,
)

PERCENT_10 = PromoCode("P10", DiscountKind.PERCENT, Decimal("10"))
FIXED_200_FROM_1000 = PromoCode(
    "F200", DiscountKind.FIXED, Decimal("200"), Decimal("1000")
)


def test_percent_code_takes_share_of_subtotal():
    assert PERCENT_10.discount_for(Decimal("570")) == Decimal("57")


def test_fixed_code_gives_fixed_amount():
    assert FIXED_200_FROM_1000.discount_for(Decimal("1200")) == Decimal("200")


def test_min_subtotal_boundary_is_inclusive():
    assert FIXED_200_FROM_1000.discount_for(Decimal("1000")) == Decimal("200")


def test_code_below_min_subtotal_is_not_applicable():
    with pytest.raises(PromoCodeNotApplicableError, match="needs order from 1000"):
        FIXED_200_FROM_1000.discount_for(Decimal("999.99"))


def test_find_existing_code():
    assert (
        find_promo_code("STUDENT10", DEFAULT_PROMO_CODES).kind is DiscountKind.PERCENT
    )


def test_find_unknown_code_raises():
    with pytest.raises(UnknownPromoCodeError, match="FREE100"):
        find_promo_code("FREE100", DEFAULT_PROMO_CODES)


def test_code_lookup_is_case_sensitive():
    with pytest.raises(UnknownPromoCodeError):
        find_promo_code("student10", DEFAULT_PROMO_CODES)
