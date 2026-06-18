from decimal import Decimal

from storage import load_data
INVENTORY_FILE = "data/inventory.json"
BOOKING_FILE = "data/bookings.json"
PAYMENT_FILE = "data/payments.json"
RETURN_FILE = "data/returns.json"

def revenue_report():

    data = load_data(PAYMENT_FILE)

    payments = data.get("payments", [])

    if not payments:

        print("\nNo payment records found.")

        return

    total_revenue = 0

    payment_count = 0

    cash_total = 0

    upi_total = 0

    card_total = 0

    for payment in payments:


        amount = Decimal(str(payment.get("amount", 0)))

        method = payment.get("payment_method", "").lower()

        total_revenue += amount

        payment_count += 1

        if method == "cash":

            cash_total += amount

        elif method == "upi":

            upi_total += amount

        elif method == "card":

            card_total += amount

    print("\n===== REVENUE REPORT =====")

    print(f"\nTotal Revenue : ₹{total_revenue:.2f}")

    print(f"\nCash : ₹{cash_total:.2f}")

    print(f"UPI  : ₹{upi_total:.2f}")

    print(f"Card : ₹{card_total:.2f}")

    print(f"\nTotal Transactions : {payment_count}")

def inventory_utilization_report():

    inventory_data = load_data(INVENTORY_FILE)

    booking_data = load_data(BOOKING_FILE)

    inventory = inventory_data.get("inventory_items", [])

    bookings = booking_data.get("bookings", [])

    print("\n===== INVENTORY UTILIZATION REPORT =====")

    if len(inventory) == 0:

        print("\nNo inventory found.")

        return

    for item in inventory:

        item_id = item["item_id"]

        item_name = item["item_name"]

        total_quantity = item.get("quantity", 0)

        booked_quantity = 0

        for booking in bookings:

            if booking.get("status") == "Cancelled":

                continue

            for booked_item in booking["items"]:

                if booked_item["item_id"] == item_id:

                    booked_quantity += booked_item["quantity"]

        available_quantity = total_quantity - booked_quantity

        print("\n--------------------------------")

        print(f"Item ID : {item_id}")

        print(f"Item Name : {item_name}")

        print(f"Total Quantity : {total_quantity}")

        print(f"Booked Quantity : {booked_quantity}")

        print(f"Available Quantity : {available_quantity}")

def reports_menu():

    while True:

        print("\n===== REPORTS =====")

        print("1. Revenue Report")

        print("2. Inventory Utilization Report")

        print("3. Back")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":

            revenue_report()

        elif choice == "2":

            inventory_utilization_report()

        elif choice == "3":

            break

        else:

            print("\nInvalid choice.")