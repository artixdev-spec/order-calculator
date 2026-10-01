# order-core

Переиспользуемый пакет с доменной логикой расчёта заказа. Не зависит от
веб-фреймворков, базы данных и переменных окружения — только стандартная
библиотека Python.

```python
from decimal import Decimal
from order_core import Order, OrderItem, calculate_receipt

order = Order(items=[OrderItem("coffee", Decimal("150"), 2)], promo_code="STUDENT10")
receipt = calculate_receipt(order)
print(receipt.total)  # 570.00
```

Сборка: `python -m build packages/core` (результат в `packages/core/dist/`).
