# Справочник API

## HTTP

Интерактивная документация OpenAPI доступна у запущенного приложения:
<http://localhost:8000/docs>.

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/health` | проверка живости |
| `GET` | `/promo-codes` | действующие промокоды |
| `POST` | `/quote` | расчёт стоимости заказа |

Пример:

```bash
curl -X POST http://localhost:8000/quote \
  -H "Content-Type: application/json" \
  -d '{"items": [{"sku": "coffee", "price": 150, "quantity": 2}], "promo_code": "STUDENT10"}'
```

```json
{"subtotal": "300.00", "discount": "30.00", "delivery": "300.00", "total": "570.00"}
```

## Пакет `order_core`

```{eval-rst}
.. automodule:: order_core.models
   :members:

.. automodule:: order_core.promo
   :members:

.. automodule:: order_core.pricing
   :members:

.. automodule:: order_core.errors
   :members:
```

## Пакет `order_api`

```{eval-rst}
.. automodule:: order_api.main
   :members: create_app

.. automodule:: order_api.promo_repository
   :members:

.. automodule:: order_api.settings
   :members:
```
