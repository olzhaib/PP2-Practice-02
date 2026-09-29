import json

with open("sample-data.json", "r") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<5}")
print("-" * 80)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]

    print(
        f"{attributes['dn']:<50} "
        f"{attributes['descr']:<20} "
        f"{attributes['speed']:<8} "
        f"{attributes['mtu']:<5}"
    )