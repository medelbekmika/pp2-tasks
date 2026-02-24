import json
with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 90)
print(f"{'DN':55} {'Description':15} {'Speed':10} {'MTU':5}")
print("-" * 90)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]

    dn = attr["dn"]
    description = attr["descr"]
    speed = attr["speed"]
    mtu = attr["mtu"]

    print(f"{dn:55} {description:15} {speed:10} {mtu:5}")
