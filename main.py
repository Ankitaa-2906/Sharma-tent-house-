from inventory_service import (
    add_inventory_item,
    view_inventory
)

from customer_service import (
    add_customer,
    find_customer,
    view_customers
)
from booking_service import (
    create_booking,
    view_bookings,
    update_booking,
)

from payment_service import (
    record_payment,
    view_payments,
    search_payment_by_booking
)

def main_menu():

    while True:

        print("\n===== SHARMA TENT HOUSE =====")
        print("1. Add Inventory Item")
        print("2. View Inventory")
        print("3. Add Customer")
        print("4. View Customers")
        print("5. Create Booking")
        print("6. View Bookings")
        print("7. Update Booking")
        print("8. Find Customer")
        print("9. Record Payment")
        print("10. View Payments")
        print("11. Search Payment by Booking ID")
        print("12. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_inventory_item()

        elif choice == "2":
            view_inventory()

        elif choice == "3":
            add_customer()

        elif choice == "4":
            view_customers()

        elif choice == "5":
            create_booking()

        elif choice == "6":
            view_bookings()

        elif choice == "7":
            update_booking()

        elif choice == "8":
            find_customer()

        elif choice == "9":
            record_payment()

        elif choice == "10":
            view_payments()

        elif choice == "11":
            search_payment_by_booking()

        elif choice == "12":
            print("\nExiting program...")
            break    

        else:
            print("\nInvalid choice. Try again.\n")


if __name__ == "__main__":
    main_menu()