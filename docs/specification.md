# Спецификация

Требования пронумерованы; в скобках — тесты, которые их проверяют.

## Входные данные

**R1.** Заказ содержит хотя бы одну позицию. Пустой заказ отклоняется ошибкой
`EmptyOrderError` (`test_empty_order_is_rejected`).

**R2.** Цена позиции не меньше 0, количество — целое больше 0. Иначе —
`InvalidItemError` (`test_negative_price_is_rejected`,
`test_non_positive_quantity_is_rejected`). Товар с нулевой ценой допустим
(`test_free_item_is_allowed`).

## Расчёт

**R3.** Сумма товаров — сумма «цена × количество» по всем позициям
(`test_order_without_discounts_pays_delivery`).

**R4.** При 10 и более единицах товара в заказе — скидка 5% от суммы товаров; при 9 —
скидки нет (`test_volume_discount_starts_from_ten_units`,
`test_volume_discount_counts_units_across_items`).

**R5.** Процентный промокод даёт скидку в процентах от суммы товаров,
фиксированный — заданную сумму (`test_percent_code_takes_share_of_subtotal`,
`test_fixed_code_gives_fixed_amount`).

**R6.** Если у промокода есть минимальная сумма заказа, при сумме товаров
**ровно** на этой границе код действует, ниже — `PromoCodeNotApplicableError`
(`test_min_subtotal_boundary_is_inclusive`,
`test_code_below_min_subtotal_is_not_applicable`).

**R7.** Неизвестный промокод — `UnknownPromoCodeError`; коды чувствительны к
регистру (`test_find_unknown_code_raises`, `test_code_lookup_is_case_sensitive`).
Пустая строка вместо промокода означает «без промокода»
(`test_empty_promo_code_is_ignored`).

**R8.** Скидка за объём и по промокоду суммируются
(`test_volume_and_promo_discounts_add_up`), но общая скидка не превышает сумму
товаров (`test_discount_never_exceeds_subtotal`).

**R9.** Доставка 300 ₽, бесплатно при сумме **после скидок** от 3000 ₽ включительно
(`test_free_delivery_boundary_is_inclusive`,
`test_free_delivery_is_checked_after_discount`).

**R10.** Все суммы в чеке округлены до копеек, половина — вверх
(`test_money_rounds_half_up_to_cents`).

## HTTP API

**R11.** `POST /quote` с корректным заказом возвращает 200 и чек
(`test_quote_returns_receipt`).

**R12.** Нарушение правил R1, R2, R6, R7 — ответ 422 с полями `error` (тип ошибки)
и `detail` (`test_domain_errors_return_422_with_error_type`). Запрос неверной
структуры — 422 от валидации (`test_malformed_request_is_rejected_by_validation`).

**R13.** `GET /promo-codes` возвращает промокоды из хранилища; расчёт использует
то же хранилище (`test_promo_codes_come_from_repository`).

**R14.** При заданной переменной `DATABASE_URL` промокоды читаются из PostgreSQL,
иначе используются встроенные (`test_settings.py`,
`tests/integration/test_postgres_repository.py`).
