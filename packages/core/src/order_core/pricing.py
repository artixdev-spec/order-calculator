"""Расчёт стоимости заказа.

Порядок расчёта:

1. ``subtotal`` — сумма всех позиций.
2. Скидка за объём: 5% от ``subtotal``, если в заказе от 10 единиц товара.
3. Скидка по промокоду (считается от ``subtotal``, суммируется со скидкой за объём).
4. Скидка не может превышать ``subtotal``.
5. Доставка 300 ₽, бесплатно — если сумма после скидок от 3000 ₽.
"""

from collections.abc import Mapping
from decimal import Decimal

from order_core.errors import EmptyOrderError
from order_core.models import Order, Receipt, money
from order_core.promo import DEFAULT_PROMO_CODES, PromoCode, find_promo_code

VOLUME_DISCOUNT_MIN_QUANTITY = 10
VOLUME_DISCOUNT_PERCENT = Decimal("5")
DELIVERY_FEE = Decimal("300")
FREE_DELIVERY_FROM = Decimal("3000")


def volume_discount(order: Order, subtotal: Decimal) -> Decimal:
    """Скидка за объём: 5% при общем количестве от 10 единиц."""
    quantity = sum(item.quantity for item in order.items)
    if quantity >= VOLUME_DISCOUNT_MIN_QUANTITY:
        return subtotal * VOLUME_DISCOUNT_PERCENT / 100
    return Decimal("0")


def delivery_fee(amount_after_discount: Decimal) -> Decimal:
    """Стоимость доставки: бесплатно от 3000 ₽, иначе 300 ₽."""
    if amount_after_discount >= FREE_DELIVERY_FROM:
        return Decimal("0")
    return DELIVERY_FEE


def calculate_receipt(
    order: Order, promo_codes: Mapping[str, PromoCode] = DEFAULT_PROMO_CODES
) -> Receipt:
    """Рассчитать чек заказа.

    :param order: заказ
    :param promo_codes: справочник промокодов (по умолчанию встроенный)
    :return: чек с суммами, округлёнными до копеек
    :raises EmptyOrderError: если в заказе нет позиций
    :raises UnknownPromoCodeError: если промокод не найден
    :raises PromoCodeNotApplicableError: если промокод не подходит к заказу
    """
    if not order.items:
        raise EmptyOrderError("order is empty")

    subtotal = sum((item.amount for item in order.items), Decimal("0"))
    discount = volume_discount(order, subtotal)
    if order.promo_code:
        promo = find_promo_code(order.promo_code, promo_codes)
        discount += promo.discount_for(subtotal)
    discount = min(discount, subtotal)

    after_discount = subtotal - discount
    delivery = delivery_fee(after_discount)
    return Receipt(
        subtotal=money(subtotal),
        discount=money(discount),
        delivery=money(delivery),
        total=money(after_discount + delivery),
    )
