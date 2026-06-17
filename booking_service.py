from storage import load_data, save_data
from utils import read_date
from datetime import datetime

from customer_service import (
    view_customers,
    find_customer
)

from inventory_service import (
    view_inventory,
    find_inventory_item
)

BOOKING_FILE = "data/bookings.json"
CUSTOMER_FILE = "data/customers.json"


def generate_booking_id(bookings):
    if not bookings:
        return "BOOK101"

    last_number = max(
        int(booking["booking_id"].replace("BOOK", ""))
        for booking in bookings
    )

    return f"BOOK{last_number + 1}"

def check_booking_availability(start_date, end_date):

    data = load_data(BOOKING_FILE)
    bookings = data.get("bookings", [])

    new_start = datetime.strptime(start_date, "%Y-%m-%d")
    new_end = datetime.strptime(end_date, "%Y-%m-%d")

    for booking in bookings:

        if booking.get("status") == "Cancelled":
            continue

        booked_start = datetime.strptime(
            booking["start_date"], "%Y-%m-%d"
        )

        booked_end = datetime.strptime(
            booking["end_date"], "%Y-%m-%d"
        )

        if new_start <= booked_end and new_end >= booked_start:

            print("\nWarning!")
            print(f"Booking {booking['booking_id']} overlaps with these dates.")
            print(f"Existing Booking: {booking['start_date']} to {booking['end_date']}")

            choice = input("\nContinue anyway? (Y/N): ").strip().upper()

            return choice == "Y"

    return True


def create_booking():
    booking_data = load_data(BOOKING_FILE)
    customer_data = load_data(CUSTOMER_FILE)

    bookings = booking_data.get("bookings", [])
    customers = customer_data.get("customers", [])

    booking_id = generate_booking_id(bookings)

    print(f"\nGenerated Booking ID: {booking_id}")

    print("\n===== AVAILABLE CUSTOMERS =====")
    view_customers()

    search_choice = input(
        "\nSearch customer first? (y/n): "
    ).strip().lower()

    if search_choice == "y":
       customer_id = find_customer()
    else:
       customer_id = input(
            "\nEnter Customer ID: "
        ).strip()

    if customer_id is None or customer_id == "":
        return

    customer_exists = False

    for customer in customers:
        if customer["customer_id"] == customer_id:
            customer_exists = True
            break

    if not customer_exists:
        print("\nCustomer ID not found. Please add customer first.\n")
        return

    event_name = input("Enter Event Name: ").strip()
    event_address = input("Enter Event Address: ").strip()


    while True:

        start_date = read_date(
            "Enter Start Date (YYYY-MM-DD): "
        )

        end_date = read_date(
            "Enter End Date (YYYY-MM-DD): "
        )
        if not check_booking_availability(start_date, end_date):

            print("\nBooking cancelled.")

            return

        start_obj = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

        end_obj = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        )

        today = datetime.today().date()
        if start_obj.date() < today:

            print(
                "\nBooking date cannot be in the past.\n"
            )

            continue

       

        if end_obj < start_obj:

            print(
                "\nError: End Date cannot be earlier than Start Date.\n"
            )

            continue

        break


    items = []

    print("\n===== AVAILABLE INVENTORY =====")
    view_inventory()
    while True:
        search_item = input(
            "\nSearch item first? (y/n): "
        ).strip().lower()

        if search_item == "y":
            item_id = find_inventory_item()
            if item_id is None:
                continue
        else:
            item_id = input(
                "Enter Item ID (or type CANCEL): "
            ).strip()
            if item_id.upper() == "CANCEL":
                print("\nBooking cancelled.\n")
                return

        try:
            quantity = int(input("Enter Quantity: "))
            if quantity <= 0:
                print("Quantity must be positive.")
                continue
        except ValueError:
            print("Invalid quantity.")
            continue

        if not check_availability(
            item_id,
            quantity,
            start_date,
            end_date
        ):
            print("Insufficient inventory or invalid Item ID.")
            continue

        items.append({
            "item_id": item_id,
            "quantity": quantity
        })

        more = input(
            "Add another item? (y/n): "
        ).strip().lower()

        if more != "y":
            break

    if len(items) == 0:
        print("\nCannot create booking without items.\n")
        return
    new_booking = {
            "booking_id": booking_id,
            "customer_id": customer_id,
            "event_name": event_name,
            "event_address": event_address,
            "start_date": start_date,
            "end_date": end_date,
            "status": "confirmed",
            "items": items
        }
    bookings.append(new_booking)

    booking_data["bookings"] = bookings

    save_data(BOOKING_FILE, booking_data)

    print("\n===== BOOKING SUMMARY =====")

    print(
        f"Booking ID   : "
        f"{booking_id}"
    )

    print(
        f"Customer ID  : "
        f"{customer_id}"
    )

    print(
        f"Event Name   : "
        f"{event_name}"
    )

    print(
        f"Address      : "
        f"{event_address}"
    )

    print(
        f"Start Date   : "
        f"{start_date}"
    )

    print(
        f"End Date     : "
        f"{end_date}"
    )

    print(
        f"Status       : Active"
    )

    print("\nItems:")

    for item in items:

        print(
            f"{item['item_id']} | "
            f"Qty: {item['quantity']}"
        )

    print(
        "\nBooking created successfully."
    )
    
def view_bookings():
    data = load_data(BOOKING_FILE)

    bookings = data.get("bookings", [])

    if not bookings:
        print("\nNo bookings found.\n")
        return

    print("\n===== BOOKINGS =====\n")

    for booking in bookings:
        print(f"Booking ID: {booking['booking_id']}")
        print(f"Customer ID: {booking['customer_id']}")
        print(f"Event: {booking['event_name']}")
        print(f"Event Address: {booking['event_address']}")
        print(f"Start Date: {booking['start_date']}")
        print(f"End Date: {booking['end_date']}")
        print(f"Status: {booking.get('status', 'confirmed')}")
        print("Items:")

        for item in booking["items"]:
            print(
                f"  {item['item_id']} - Qty: {item['quantity']}"
            )

        print("-" * 40)

def customer_booking_history():

    data = load_data(BOOKING_FILE)

    bookings = data.get("bookings", [])

    customer_id = input("\nEnter Customer ID: ").strip()

    found = False

    print("\n===== CUSTOMER BOOKING HISTORY =====")

    for booking in bookings:

        if booking["customer_id"] == customer_id:

            found = True

            print("\n-----------------------------")

            print(f"Booking ID : {booking['booking_id']}")

            print(f"Event : {booking['event_name']}")

            print(f"Start Date : {booking['start_date']}")

            print(f"End Date : {booking['end_date']}")

            print(f"Status : {booking.get('status', 'Confirmed')}")

    if not found:

        print("\nNo bookings found for this customer.")

def update_booking_status():

    data = load_data(
        BOOKING_FILE
    )

    bookings = data.get(
        "bookings",
        []
    )

    booking_id = input(
        "\nEnter Booking ID: "
    ).strip()

    booking_found = None

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            booking_found = booking

            break

    if booking_found is None:

        print(
            "\nBooking not found."
        )

        return

    print(
        f"\nCurrent Status: "
        f"{booking_found.get('status', 'Confirmed')}"
    )

    print("\nAvailable Statuses")

    print("1. Pending")
    print("2. Confirmed")
    print("3. Completed")
    print("4. Cancelled")
    print("5. Returned")

    choice = input(
        "\nSelect Status: "
    ).strip()

    status_map = {

        "1": "Pending",

        "2": "Confirmed",

        "3": "Completed",

        "4": "Cancelled",

        "5": "Returned"

    }

    if choice not in status_map:

        print(
            "\nInvalid status."
        )

        return

    booking_found["status"] = (
        status_map[choice]
    )

    save_data(
        BOOKING_FILE,
        data
    )

    print(
        "\nBooking status updated successfully."
    )

    print(
        f"New Status: "
        f"{booking_found['status']}"
    )

def update_booking():

    data = load_data(BOOKING_FILE)

    bookings = data.get("bookings", [])

    booking_id = input(
        "\nEnter Booking ID: "
    ).strip()

    booking_found = None

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            booking_found = booking
            break

    if booking_found is None:

        print("\nBooking not found.")
        return

    while True:

        print("\n===== UPDATE BOOKING =====")

        print("1. Update Event Name")
        print("2. Update Event Address")
        print("3. Add Item")
        print("4. Change Item Quantity")
        print("5. Remove Item")
        print("6. Cancel Booking")
        print("7. Save and Exit")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            booking_found["event_name"] = input(
                "Enter New Event Name: "
            ).strip()

        elif choice == "2":

            booking_found["event_address"] = input(
                "Enter New Address: "
            ).strip()

        elif choice == "3":

            add_item_to_booking(
                booking_found
            )

        elif choice == "4":

            update_item_quantity(
                booking_found
            )

        elif choice == "5":

            remove_item_from_booking(
                booking_found
            )

        elif choice == "6":

            booking_found["status"] = "cancelled"

            print(
                "\nBooking cancelled."
            )

        elif choice == "7":

            save_data(
                BOOKING_FILE,
                data
            )

            print(
                "\nBooking updated successfully."
            )

            return

        else:

            print(
                "\nInvalid choice."
            )
def add_item_to_booking(booking):

    view_inventory()

    item_id = input(
        "\nEnter Item ID: "
    ).strip()

    try:

        quantity = int(
            input("Enter Quantity: ")
        )

        if quantity <= 0:

            print(
                "Quantity must be positive."
            )
            return

    except ValueError:

        print(
            "Invalid quantity."
        )
        return

    booking["items"].append({

        "item_id": item_id,
        "quantity": quantity

    })

    print(
        "\nItem added successfully."
    )
def update_item_quantity(booking):

    for item in booking["items"]:

        print(
            f"{item['item_id']} "
            f"- Qty: {item['quantity']}"
        )

    item_id = input(
        "\nEnter Item ID: "
    ).strip()

    for item in booking["items"]:

        if item["item_id"] == item_id:

            try:

                new_quantity = int(
                    input(
                        "Enter New Quantity: "
                    )
                )

                if new_quantity <= 0:

                    print(
                        "Quantity must be positive."
                    )
                    return

            except ValueError:

                print(
                    "Invalid quantity."
                )
                return

            item["quantity"] = new_quantity

            print(
                "\nQuantity updated successfully."
            )

            return

    print(
        "\nItem not found."
    )
def remove_item_from_booking(booking):

    for item in booking["items"]:

        print(
            f"{item['item_id']} "
            f"- Qty: {item['quantity']}"
        )

    item_id = input(
        "\nEnter Item ID to remove: "
    ).strip()

    for item in booking["items"]:

        if item["item_id"] == item_id:

            booking["items"].remove(item)

            print(
                "\nItem removed successfully."
            )

            return

    print(
        "\nItem not found."
    )

def check_availability(
    item_id,
    requested_quantity,
    start_date,
    end_date
):

    inventory_data = load_data(
        "data/inventory.json"
    )

    booking_data = load_data(
        BOOKING_FILE
    )

    inventory_items = inventory_data.get(
        "inventory_items",
        []
    )

    bookings = booking_data.get(
        "bookings",
        []
    )

    quantity = 0

    for item in inventory_items:

        if item["item_id"] == item_id:

            quantity = item[
                "quantity"
            ]

            break

    if quantity == 0:

        return False

    booked_quantity = 0

    request_start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    request_end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    for booking in bookings:

        if booking["status"] == "cancelled":
            continue

        booking_start = datetime.strptime(
            booking["start_date"],
            "%Y-%m-%d"
        )

        booking_end = datetime.strptime(
            booking["end_date"],
            "%Y-%m-%d"
        )

        overlap = (

            request_start <= booking_end

            and

            request_end >= booking_start

        )

        if overlap:

            for booked_item in booking["items"]:

                if (
                    booked_item["item_id"]
                    == item_id
                ):

                    booked_quantity += (
                        booked_item["quantity"]
                    )

    available_quantity = (
        quantity
        - booked_quantity
    )

    return (
        requested_quantity
        <= available_quantity
    )
def booking_menu():

    while True:

        print("\n===== BOOKING MANAGEMENT =====")

        print("1. Create Booking")
        print("2. View Bookings")
        print("3. Customer Booking History")
        print("4. Update Booking Status")
        print("5. Update Booking")
        print("6. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            create_booking()

        elif choice == "2":

            view_bookings()

        elif choice == "3":

            customer_booking_history()

        elif choice == "4":

            update_booking_status()


        elif choice == "5":

            update_booking()

        elif choice == "6":

            break

        else:

            print("\nInvalid choice.")