from storage import load_data, save_data

INVENTORY_FILE = "data/inventory.json"


def add_inventory_item():
    """
    Adds a new inventory item to the system.
    """

    data = load_data(INVENTORY_FILE)

    inventory_items = data.get("inventory_items", [])

    print("\n===== ADD INVENTORY ITEM =====\n")

    item_id = input("Enter Item ID: ").strip()

    for item in inventory_items:
     if item["item_id"] == item_id:
        print("\nItem ID already exists.\n")
        return
     
    item_name = input("Enter Item Name: ").strip()
    category = input("Enter Category: ").strip()

    try:
        total_quantity = int(input("Enter Total Quantity: "))

        if total_quantity <= 0:
            print("\nQuantity must be greater than zero.\n")
            return

        price_per_day = float(input("Enter Price Per Day: "))

        if price_per_day < 0:
            print("\nPrice cannot be negative.\n")
            return

    except ValueError:
        print("\nInvalid numeric input.\n")
        return

    new_item = {
        "item_id": item_id,
        "item_name": item_name,
        "category": category,
        "total_quantity": total_quantity,
        "price_per_day": price_per_day,
        "tracking_type": tracking_type
    }

    inventory_items.append(new_item)

    data["inventory_items"] = inventory_items

    save_data(INVENTORY_FILE, data)

    print("\nInventory item added successfully.\n")


def view_inventory():
    """
    Displays all inventory items.
    """

    data = load_data(INVENTORY_FILE)

    inventory_items = data.get("inventory_items", [])

    if not inventory_items:
        print("\nNo inventory items found.\n")
        return

    print("\n===== INVENTORY ITEMS =====\n")

    for item in inventory_items:

        print(f"Item ID: {item['item_id']}")
        print(f"Name: {item['item_name']}")
        print(f"Category: {item['category']}")
        print(f"Quantity: {item['total_quantity']}")
        print(f"Price Per Day: ₹{item['price_per_day']}")
        print(f"Tracking Type: {item['tracking_type']}")

        print("-" * 40)