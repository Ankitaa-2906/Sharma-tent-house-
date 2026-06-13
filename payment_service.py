from customer_service import find_customer
from storage import load_data, save_data
from datetime import datetime

PAYMENT_FILE = "data/payments.json"
BOOKING_FILE = "data/bookings.json"


def generate_payment_id(payments):
    """
    Generates unique Payment IDs:
    P101, P102, P103...
    """

    if not payments:
        return "P101"

    last_number = max(
        int(payment["payment_id"].replace("P", ""))
        for payment in payments
    )

    return f"P{last_number + 1}"

from decimal import Decimal

def find_booking_for_customer(customer_id):

    booking_data = load_data(
        BOOKING_FILE
    )

    bookings = booking_data.get(
        "bookings",
        []
    )

    customer_bookings = []

    for booking in bookings:

        if booking["customer_id"] == customer_id:

            customer_bookings.append(
                booking
            )

    if not customer_bookings:

        print(
            "\nNo bookings found for this customer."
        )

        return None

    print("\n===== CUSTOMER BOOKINGS =====")

    for index, booking in enumerate(
        customer_bookings,
        start=1
    ):

        print(

            f"{index}. "

            f"{booking['booking_id']} | "

            f"{booking['event_name']} | "

            f"{booking['start_date']}"

        )

    try:

        choice = int(

            input(
                "\nSelect Booking: "
            )

        )

        if (
            1 <= choice <=
            len(customer_bookings)
        ):

            return customer_bookings[
                choice - 1
            ]

    except ValueError:

        pass

    print(
        "\nInvalid selection."
    )

    return None

def record_payment():

    payment_data = load_data(PAYMENT_FILE)
    booking_data = load_data(BOOKING_FILE)

    payments = payment_data.get("payments", [])
    bookings = booking_data.get("bookings", [])

    payment_id = generate_payment_id(payments)

    print(f"\nGenerated Payment ID: {payment_id}")

    print("\nSearch Customer")

    customer_id = find_customer()

    if customer_id is None:

        return
    selected_booking = find_booking_for_customer(
            customer_id
        )

    if selected_booking is None:

            return

    try:
        amount = Decimal(input("Enter Amount: ").strip())
    except Exception:
        print("\nInvalid amount.")
        return

    if amount <= 0:
        print("\nAmount must be positive.")
        return

    while True:

        payment_method = input(
            "Enter Payment Method (Cash/UPI/Card): "
        ).strip().lower()

        valid_methods = {
            "cash": "Cash",
            "upi": "UPI",
            "card": "Card"
        }

        if payment_method in valid_methods:

            payment_method = valid_methods[
                payment_method
            ]

            break

        print(
            "Invalid payment method. "
            "Please enter Cash, UPI or Card."
        )

    payment_status = "Paid"

    new_payment = {
    "payment_id": payment_id,
    "customer_id": customer_id,
    "booking_id": selected_booking["booking_id"],
    "amount": str(amount),
    "payment_method": payment_method,
    "status": payment_status,
    "payment_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

    payments.append(new_payment)

    payment_data["payments"] = payments


    save_data(
        PAYMENT_FILE,
        payment_data
    )

    print("\n===== PAYMENT SUMMARY =====")

    print(
        f"Payment ID : "
        f"{payment_id}"
    )

    print(
        f"Customer ID : "
        f"{customer_id}"
    )

    print(
        f"Booking ID  : "
        f"{selected_booking['booking_id']}"
    )

    print(
        f"Amount     : "
        f"{amount}"
    )

    print(
        f"Method     : "
        f"{payment_method}"
    )

    print(
        f"Status     : "
        f"{payment_status}"
    )
    print(
        f"Date/Time  : "
        f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    )

    print(
        "\nPayment recorded successfully."
    )

def view_payments():

    data = load_data(PAYMENT_FILE)

    payments = data.get(
        "payments",
        []
    )

    if not payments:
        print(
            "\nNo payments found.\n"
        )
        return

    print(
        "\n===== PAYMENTS =====\n"
    )

    for payment in payments:

        print(
            f"Payment ID: "
            f"{payment['payment_id']}"
        )

        print(
            f"Customer ID: "
            f"{payment['customer_id']}"
        )
        
        print(
            f"Amount: ₹"
            f"{payment['amount']}"
        )

        print(
            f"Method: "
            f"{payment['payment_method']}"
        )

        print(
            f"Status: "
            f"{payment['status']}"
        )

        print("-" * 40)

def search_payment_by_customer():

        print("\nSearch Customer")

        customer_id = find_customer()

        if customer_id is None:

         return

        data = load_data(PAYMENT_FILE)

        payments = data.get("payments", [])

        found = False

        for payment in payments:

         if payment["customer_id"] == customer_id:

            print("\nPayment Found:\n")

            print(
                f"Payment ID: "
                f"{payment['payment_id']}"
            )

            print(
                f"Customer ID: "
                f"{payment.get('customer_id', 'N/A')}"
            )

            print(
                f"Booking ID: "
                f"{payment.get('booking_id', 'N/A')}"
            )

            print(
                f"Amount: ₹"
                f"{payment['amount']}"
            )

            print(
                f"Method: "
                f"{payment['payment_method']}"
            )

            print(
                f"Status: "
                f"{payment.get('status', 'Paid')}"
            )

            print("-" * 40)

            found = True

        if not found:
         print(
            "\nNo payment found "
            "for this Customer ID."
        )
def payment_menu():

    while True:

        print("\n===== PAYMENT MANAGEMENT =====")

        print("1. Record Payment")
        print("2. View Payments")
        print("3. Search Payment by Customer")
        print("4. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            record_payment()

        elif choice == "2":

            view_payments()

        elif choice == "3":

            search_payment_by_customer()

        elif choice == "4":

            return

        else:

            print("\nInvalid choice.")