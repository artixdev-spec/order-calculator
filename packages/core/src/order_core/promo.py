"""Промокоды: процентные и фиксированные, с минимальной суммой заказа."""

from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from order_core.errors import PromoCodeNotApplicableError, UnknownPromoCodeError


class DiscountKind(Enum):
    PERCENT = "percent"
    FIXED = "fixed"


@dataclass(frozen=True)
class PromoCode:
    """Промокод.

    :param code: текст промокода, например ``STUDENT10``
    :param kind: процент от суммы или фиксированная сумма
    :param value: размер скидки — процент (0–100) или сумма в рублях
    :param min_subtotal: минимальная сумма заказа, с которой код действует
    """

    code: str
    kind: DiscountKind
    value: Decimal
    min_subtotal: Decimal = Decimal("0")

    def discount_for(self, subtotal: Decimal) -> Decimal:
        """Скидка по этому коду для заказа на сумму ``subtotal``.

        :raises PromoCodeNotApplicableError: если сумма меньше ``min_subtotal``
        """
        if subtotal < self.min_subtotal:
            raise PromoCodeNotApplicableError(
                f"{self.code} needs order from {self.min_subtotal}"
            )
        if self.kind is DiscountKind.PERCENT:
            return subtotal * self.value / 100
        return self.value


DEFAULT_PROMO_CODES: dict[str, PromoCode] = {
    "STUDENT10": PromoCode("STUDENT10", DiscountKind.PERCENT, Decimal("10")),
    "WELCOME200": PromoCode(
        "WELCOME200", DiscountKind.FIXED, Decimal("200"), Decimal("1000")
    ),
}


def find_promo_code(code: str, promo_codes: Mapping[str, PromoCode]) -> PromoCode:
    """Найти промокод в справочнике.

    :raises UnknownPromoCodeError: если кода нет
    """
    try:
        return promo_codes[code]
    except KeyError:
        raise UnknownPromoCodeError(f"unknown promo code {code}") from None
