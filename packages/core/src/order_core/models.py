"""Сущности заказа."""

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from order_core.errors import InvalidItemError

CENT = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    """Округлить сумму до копеек по правилу «половина вверх»."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class OrderItem:
    """Позиция заказа.

    :param sku: артикул товара
    :param unit_price: цена за единицу, не меньше 0
    :param quantity: количество, больше 0
    :raises InvalidItemError: при отрицательной цене или неположительном количестве
    """

    sku: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self) -> None:
        if self.unit_price < 0:
            raise InvalidItemError(f"negative price for {self.sku}")
        if self.quantity <= 0:
            raise InvalidItemError(f"bad quantity for {self.sku}")

    @property
    def amount(self) -> Decimal:
        """Стоимость позиции: цена × количество."""
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class Order:
    """Заказ: позиции и необязательный промокод."""

    items: list[OrderItem] = field(default_factory=list)
    promo_code: str | None = None


@dataclass(frozen=True)
class Receipt:
    """Результат расчёта заказа. Все суммы округлены до копеек."""

    subtotal: Decimal
    discount: Decimal
    delivery: Decimal
    total: Decimal
