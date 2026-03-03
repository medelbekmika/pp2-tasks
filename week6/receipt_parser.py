#1
def parse_receipt(text):
    lines = text.split("\n")
    items = []
    for line in lines:
        if "-" in line:
            name, price = line.split("-")
            items.append((name.strip(), float(price.strip())))
    return items

#2
def calculate_total(items):
    return sum(price for _, price in items)

#3
def read_receipt(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

#4
try:
    data = read_receipt("raw.txt")
except FileNotFoundError:
    print("Файл не найден")

#5
if __name__ == "__main__":
    text = read_receipt("raw.txt")
    items = parse_receipt(text)
    total = calculate_total(items)
    print("Итого:", total)
