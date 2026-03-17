import re
import json

# Read file
with open("raw.txt", "r") as file:
    text = file.read()

# 1. Extract prices
prices = re.findall(r"\d+\.\d{2}", text)
prices = list(map(float, prices))

# 2. Extract items (name + price)
items = re.findall(r"([A-Za-z]+)\s+(\d+\.\d{2})", text)
parsed_items = [{"name": name, "price": float(price)} for name, price in items]

# 3. Calculate total
calculated_total = sum([item["price"] for item in parsed_items])

# 4. Extract date
date_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
date = date_match.group() if date_match else None

# 5. Extract time
time_match = re.search(r"\d{2}:\d{2}", text)
time = time_match.group() if time_match else None

# 6. Extract payment method
payment_match = re.search(r"Payment:\s*(\w+)", text)
payment = payment_match.group(1) if payment_match else None

# 7. Extract total from receipt
total_match = re.search(r"Total:\s*(\d+\.\d{2})", text)
total = float(total_match.group(1)) if total_match else None

# Output result
result = {
    "date": date,
    "time": time,
    "items": parsed_items,
    "calculated_total": round(calculated_total, 2),
    "receipt_total": total,
    "payment": payment
}

print(json.dumps(result, indent=4))
