from storage import load_data, save_data

INVENTORY_FILE = "data/inventory.json"

def generate_item_id(inventory_items):
    if not inventory_items:
        return "ITEM101"

    last_number = max(
        int(item["item_id"].replace("ITEM", ""))
        for item in inventory_items
    )

    return f"ITEM{last_number + 1}"


def add_inventory_item():
    """
    Adds a new inventory item to the system.
    """

    data = load_data(INVENTORY_FILE)

    inventory_items = data.get("inventory_items", [])

    print("\n===== ADD INVENTORY ITEM =====\n")

    item_id = generate_item_id(inventory_items)
    print(f"Generated Item ID: {item_id}")
     
    item_name = input("Enter Item Name: ").strip()
    for item in inventory_items:
            if item["item_name"].lower() == item_name.lower():
                print("\nItem name already exists.\n")
                return
            
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
        "tracking_type": input("Enter Tracking Type (bulk/unique_unit): ").strip()
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

def find_inventory_item():
    search = input(
        "Enter item name: "
    ).strip().lower()

    data = load_data(INVENTORY_FILE)

    items = data.get("inventory_items", [])

    matches = []

    for item in items:
        if search in item["item_name"].lower():
            matches.append(item)

    if not matches:
        print("\nItem not found.")
        return None

    print("\nMatching Items:")

    for index, item in enumerate(matches, start=1):
        print(
            f"{index}. "
            f"{item['item_id']} | "
            f"{item['item_name']}"
        )

    try:
        choice = int(
            input("\nSelect item number: ")
        )

        if 1 <= choice <= len(matches):
            return matches[choice - 1]["item_id"]

    except ValueError:
        pass

    print("Invalid selection.")
    return None

def update_inventory_item():

    data = load_data(INVENTORY_FILE)

    items = data.get(
        "inventory_items",
        []
    )

    item_id = input(
        "\nEnter Item ID: "
    ).strip()

    for item in items:

        if item["item_id"] == item_id:

            print(
                f"\nCurrent Name: "
                f"{item['item_name']}"
            )

            print(
                f"Current Quantity: "
                f"{item['quantity']}"
            )

            new_name = input(
                "Enter New Item Name: "
            ).strip()

            try:

                new_quantity = int(
                    input(
                        "Enter New Quantity: "
                    )
                )

            except ValueError:

                print(
                    "Invalid quantity."
                )

                return

            item["item_name"] = new_name
            item["quantity"] = new_quantity

            save_data(
                INVENTORY_FILE,
                data
            )

            print(
                "\nInventory updated successfully."
            )

            return

    print(
        "\nItem ID not found."
    )

def delete_inventory_item():

    data = load_data(
        INVENTORY_FILE
    )

    items = data.get(
        "inventory_items",
        []
    )

    item_id = input(
        "\nEnter Item ID: "
    ).strip()

    for item in items:

        if item["item_id"] == item_id:

            items.remove(item)

            save_data(
                INVENTORY_FILE,
                data
            )

            print(
                "\nItem deleted successfully."
            )

            return

    print(
        "\nItem ID not found."
    )

def inventory_menu():

    while True:

        print("\n===== INVENTORY MANAGEMENT =====")

        print("1. Add Item")
        print("2. View Inventory")
        print("3. Find Item")
        print("4. Update Item")
        print("5. Delete Item")
        print("6. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            add_inventory_item()

        elif choice == "2":

            view_inventory()

        elif choice == "3":

            find_inventory_item()

        elif choice == "4":

            update_inventory_item()

        elif choice == "5":

            delete_inventory_item()

        elif choice == "6":

            return

        else:

            print("\nInvalid choice.")