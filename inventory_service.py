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
        quantity = int(input("Enter Total Quantity: "))

        if quantity <= 0:
            print("\nQuantity must be greater than zero.\n")
            return
        damage_charge = float( input("Enter Damage Charge Per Item: ") )

        replacement_cost = float(input("Enter Replacement Cost Per Item: "))

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
        "quantity": quantity,
        "damage_charge": damage_charge,
        "replacement_cost": replacement_cost,
        "price_per_day": price_per_day,
        "tracking_type": input("Enter Tracking Type (bulk/unique_unit): ").strip()
    }

    inventory_items.append(new_item)

    data["inventory_items"] = inventory_items

    save_data(INVENTORY_FILE, data)

    print("\n===== INVENTORY SUMMARY =====")

    print(
        f"Item ID   : "
        f"{item_id}"
    )

    print(
        f"Item Name : "
        f"{item_name}"
    )

    print(
        f"Quantity  : "
        f"{quantity}"
    )

    print(
        "\nItem added successfully."
    )


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
        print(f"Quantity: {item['quantity']}")
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

    item_found = None

    for item in items:

        if item["item_id"] == item_id:

            item_found = item
            break

    if item_found is None:

        print(
            "\nItem ID not found."
        )

        return

    while True:

        print("\n===== CURRENT DETAILS =====")

        print(
            f"Name: "
            f"{item_found['item_name']}"
        )

        print(
            f"Category: "
            f"{item_found['category']}"
        )

        print(
            f"Price Per Day: "
            f"{item_found['price_per_day']}"
        )

        print(
            f"Tracking Type: "
            f"{item_found['tracking_type']}"
        )

        print(
            f"Quantity: "
            f"{item_found['total_quantity']}"
        )

        print("\n===== UPDATE INVENTORY =====")

        print("1. Update Name")
        print("2. Update Category")
        print("3. Update Price Per Day")
        print("4. Update Tracking Type")
        print("5. Update Quantity")
        print("6. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            while True:

                new_name = input(
                    "Enter New Name: "
                ).strip()

                if not new_name:

                    print(
                        "Name cannot be empty."
                    )

                    continue

                item_found[
                    "item_name"
                ] = new_name.title()

                save_data(
                    INVENTORY_FILE,
                    data
                )

                print(
                    "\nName updated successfully."
                )

                break

        elif choice == "2":

            while True:

                new_category = input(
                    "Enter New Category: "
                ).strip()

                if not new_category:

                    print(
                        "Category cannot be empty."
                    )

                    continue

                item_found[
                    "category"
                ] = new_category.title()

                save_data(
                    INVENTORY_FILE,
                    data
                )

                print(
                    "\nCategory updated successfully."
                )

                break

        elif choice == "3":

            while True:

                try:

                    new_price = float(
                        input(
                            "Enter New Price Per Day: "
                        )
                    )

                    if new_price <= 0:

                        print(
                            "Price must be greater than zero."
                        )

                        continue

                    item_found[
                        "price_per_day"
                    ] = new_price

                    save_data(
                        INVENTORY_FILE,
                        data
                    )

                    print(
                        "\nPrice updated successfully."
                    )

                    break

                except ValueError:

                    print(
                        "Invalid price."
                    )

        elif choice == "4":

            while True:

                tracking_type = input(
                    "Enter Tracking Type (bulk/unit): "
                ).strip().lower()

                if tracking_type not in [
                    "bulk",
                    "unit"
                ]:

                    print(
                        "Enter bulk or unit only."
                    )

                    continue

                item_found[
                    "tracking_type"
                ] = tracking_type

                save_data(
                    INVENTORY_FILE,
                    data
                )

                print(
                    "\nTracking Type updated successfully."
                )

                break

        elif choice == "5":

            while True:

                try:

                    new_quantity = int(
                        input(
                            "Enter New Quantity: "
                        )
                    )

                    if new_quantity < 0:

                        print(
                            "Quantity cannot be negative."
                        )

                        continue

                    item_found[
                        "total_quantity"
                    ] = new_quantity

                    save_data(
                        INVENTORY_FILE,
                        data
                    )

                    print(
                        "\nQuantity updated successfully."
                    )

                    break

                except ValueError:

                    print(
                        "Invalid quantity."
                    )

        elif choice == "6":

            return

        else:

            print(
                "\nInvalid choice."
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