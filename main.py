from inventory_service import (
    add_inventory_item,
    view_inventory
)


def main_menu():

    while True:

        print("\n===== SHARMA TENT HOUSE =====")
        print("1. Add Inventory Item")
        print("2. View Inventory")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_inventory_item()

        elif choice == "2":
            view_inventory()

        elif choice == "3":
            print("\nExiting program...")
            break

        else:
            print("\nInvalid choice. Try again.\n")


if __name__ == "__main__":
    main_menu()