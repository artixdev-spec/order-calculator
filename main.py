import json
import sys

# заказ в JSON: {"items": [{"sku": "coffee", "price": 150, "quantity": 2}], "promo_code": "STUDENT10"}

if len(sys.argv) < 2:
    print("usage: python main.py order.json")
    sys.exit(1)

data = json.load(open(sys.argv[1], encoding="utf-8"))

items = data.get("items", [])
if not items:
    print("error: order is empty")
    sys.exit(1)

subtotal = 0
qty = 0
for it in items:
    if it["price"] < 0:
        print("error: negative price for " + it["sku"])
        sys.exit(1)
    if it["quantity"] <= 0:
        print("error: bad quantity for " + it["sku"])
        sys.exit(1)
    subtotal = subtotal + it["price"] * it["quantity"]
    qty = qty + it["quantity"]

discount = 0
# скидка за объём: от 10 штук 5%
if qty >= 10:
    discount = discount + subtotal * 0.05

code = data.get("promo_code")
if code:
    if code == "STUDENT10":
        discount = discount + subtotal * 0.10
    elif code == "WELCOME200":
        if subtotal >= 1000:
            discount = discount + 200
        else:
            print("error: WELCOME200 needs order from 1000")
            sys.exit(1)
    else:
        print("error: unknown promo code " + code)
        sys.exit(1)

if discount > subtotal:
    discount = subtotal

after = subtotal - discount
delivery = 0 if after >= 3000 else 300

total = after + delivery

print("subtotal: %.2f" % subtotal)
print("discount: %.2f" % discount)
print("delivery: %.2f" % delivery)
print("total: %.2f" % total)
