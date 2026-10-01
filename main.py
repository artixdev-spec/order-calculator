import json
import sys
from decimal import Decimal

from order_core import Order, OrderError, OrderItem, calculate_receipt


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python main.py order.json")
        return 1

    with open(sys.argv[1], encoding="utf-8") as file:
        data = json.load(file)

    try:
        order = Order(
            items=[
                OrderItem(it["sku"], Decimal(str(it["price"])), it["quantity"])
                for it in data.get("items", [])
            ],
            promo_code=data.get("promo_code"),
        )
        receipt = calculate_receipt(order)
    except OrderError as error:
        print(f"error: {error}")
        return 1

    print(f"subtotal: {receipt.subtotal}")
    print(f"discount: {receipt.discount}")
    print(f"delivery: {receipt.delivery}")
    print(f"total: {receipt.total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
