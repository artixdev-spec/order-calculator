"""Ошибки предметной области. Все наследуются от :class:`OrderError`."""


class OrderError(ValueError):
    """Базовая ошибка: заказ не может быть рассчитан."""


class EmptyOrderError(OrderError):
    """В заказе нет ни одной позиции."""


class InvalidItemError(OrderError):
    """Позиция заказа некорректна: отрицательная цена или количество не больше нуля."""


class UnknownPromoCodeError(OrderError):
    """Промокод не найден."""


class PromoCodeNotApplicableError(OrderError):
    """Промокод существует, но к этому заказу не применим (например, сумма мала)."""
