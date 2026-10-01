"""Схемы запросов и ответов API."""

from decimal import Decimal

from pydantic import BaseModel

from order_core import Order, OrderItem, PromoCode, Receipt


class ItemIn(BaseModel):
    sku: str
    price: Decimal
    quantity: int


class OrderIn(BaseModel):
    items: list[ItemIn]
    promo_code: str | None = None

    def to_domain(self) -> Order:
        """Преобразовать в доменный заказ. Валидация позиций — в ``order_core``."""
        return Order(
            items=[OrderItem(i.sku, i.price, i.quantity) for i in self.items],
            promo_code=self.promo_code,
        )


class ReceiptOut(BaseModel):
    subtotal: Decimal
    discount: Decimal
    delivery: Decimal
    total: Decimal

    @classmethod
    def from_domain(cls, receipt: Receipt) -> "ReceiptOut":
        return cls(
            subtotal=receipt.subtotal,
            discount=receipt.discount,
            delivery=receipt.delivery,
            total=receipt.total,
        )


class PromoCodeOut(BaseModel):
    code: str
    kind: str
    value: Decimal
    min_subtotal: Decimal

    @classmethod
    def from_domain(cls, promo: PromoCode) -> "PromoCodeOut":
        return cls(
            code=promo.code,
            kind=promo.kind.value,
            value=promo.value,
            min_subtotal=promo.min_subtotal,
        )


class ErrorOut(BaseModel):
    error: str
    detail: str
