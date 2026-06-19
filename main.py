from customer_service import customer_menu
from inventory_service import inventory_menu
from booking_service import booking_menu
from payment_service import payment_menu
from returns_service import return_menu
from report_service import reports_menu 

def main_menu():

    while True:

        print("\n===== SHARMA TENT HOUSE =====")

        print("1. Customer Management")
        print("2. Inventory Management")
        print("3. Booking Management")
        print("4. Payment Management")
        print("5. Return Management")
        print("6. Reports")
        print("7. Exit")

        choice = input("\nEnter Choice: ").strip()

        if choice == "1":

            customer_menu()

        elif choice == "2":

            inventory_menu()

        elif choice == "3":

            booking_menu()

        elif choice == "4":

            payment_menu()

        elif choice == "5":

            return_menu()

        elif choice == "6":

            reports_menu()

        elif choice == "7":

            print("\nThank You.")
            break

        else:

            print("\nInvalid choice.")              
if __name__ == "__main__":
    main_menu()