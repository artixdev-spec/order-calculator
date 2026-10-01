"""Хранилища промокодов. API работает с любым объектом, реализующим протокол."""

from typing import Protocol

from order_core import DEFAULT_PROMO_CODES, PromoCode


class PromoCodeRepository(Protocol):
    def all(self) -> dict[str, PromoCode]:
        """Все действующие промокоды: ``код -> PromoCode``."""
        ...


class InMemoryPromoCodeRepository:
    """Промокоды в памяти процесса. По умолчанию — встроенные из ``order_core``."""

    def __init__(self, promo_codes: dict[str, PromoCode] | None = None) -> None:
        self._promo_codes = dict(
            DEFAULT_PROMO_CODES if promo_codes is None else promo_codes
        )

    def all(self) -> dict[str, PromoCode]:
        return dict(self._promo_codes)
