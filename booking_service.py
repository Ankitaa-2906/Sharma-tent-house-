from storage import load_data, save_data
from utils import read_date

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


def create_booking():
    booking_data = load_data(BOOKING_FILE)
    customer_data = load_data(CUSTOMER_FILE)

    bookings = booking_data.get("bookings", [])
    customers = customer_data.get("customers", [])

    booking_id = generate_booking_id(bookings)

    print(f"\nGenerated Booking ID: {booking_id}")

    customer_id = input("Enter Customer ID: ").strip()

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
    from utils import read_date

    start_date = read_date("Enter Start Date (YYYY-MM-DD): ")
    end_date = read_date("Enter End Date (YYYY-MM-DD): ")

    items = []

    while True:

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

        if not check_availability(item_id, quantity):
            print("Insufficient inventory or invalid Item ID.")
            continue

        items.append({
            "item_id": item_id,
            "quantity": quantity
        })

        more = input("Add another item? (y/n): ").strip().lower()

        if more != "y":
            break

        new_booking = {
            "booking_id": booking_id,
            "customer_id": customer_id,
            "event_name": event_name,
            "event_address": event_address,
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "items": items
        }
        new_booking["items"] = items

        bookings.append(new_booking)

        booking_data["bookings"] = bookings

        save_data(BOOKING_FILE, booking_data)

    print("\nBooking created successfully.\n")
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
        print(f"Status: {booking['status']}")
        print("Items:")

        for item in booking["items"]:
         print(
        f"  {item['item_id']} - Qty: {item['quantity']}"
    )
        print("-" * 40)
from datetime import datetime


def check_availability(item_id, requested_quantity, start_date, end_date):

    inventory_data = load_data("data/inventory.json")
    booking_data = load_data(BOOKING_FILE)

    inventory_items = inventory_data.get("inventory_items", [])
    bookings = booking_data.get("bookings", [])

    total_quantity = 0

    for item in inventory_items:
        if item["item_id"] == item_id:
            total_quantity = item["total_quantity"]
            break

    if total_quantity == 0:
        return False

    booked_quantity = 0

    request_start = datetime.strptime(start_date, "%Y-%m-%d")
    request_end = datetime.strptime(end_date, "%Y-%m-%d")

    for booking in bookings:

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
            and request_end >= booking_start
        )

        if overlap:

            for booked_item in booking["items"]:

                if booked_item["item_id"] == item_id:
                    booked_quantity += booked_item["quantity"]

    available_quantity = total_quantity - booked_quantity

    return requested_quantity <= available_quantity