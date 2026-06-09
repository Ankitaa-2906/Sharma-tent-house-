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
def record_payment():

    payment_data = load_data(PAYMENT_FILE)
    booking_data = load_data(BOOKING_FILE)

    payments = payment_data.get("payments", [])
    bookings = booking_data.get("bookings", [])

    payment_id = generate_payment_id(payments)

    print(f"\nGenerated Payment ID: {payment_id}")

    booking_id = input(
        "Enter Booking ID: "
    ).strip()

    booking_exists = False

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            booking_exists = True
            break

    if not booking_exists:
        print(
            "\nBooking ID not found."
        )
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
    "booking_id": booking_id,
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

    print(
        "\nPayment recorded successfully.\n"
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
            f"Booking ID: "
            f"{payment['booking_id']}"
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

def search_payment_by_booking():

    booking_id = input(
        "Enter Booking ID: "
    ).strip()

    data = load_data(PAYMENT_FILE)

    payments = data.get("payments", [])

    found = False

    for payment in payments:

        if payment["booking_id"] == booking_id:

            print("\nPayment Found:\n")

            print(
                f"Payment ID: "
                f"{payment['payment_id']}"
            )

            print(
                f"Booking ID: "
                f"{payment['booking_id']}"
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

            found = True

    if not found:
        print(
            "\nNo payment found "
            "for this Booking ID."
        )
def payment_menu():

    while True:

        print("\n===== PAYMENT MANAGEMENT =====")

        print("1. Record Payment")
        print("2. View Payments")
        print("3. Search Payment by Booking ID")
        print("4. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            record_payment()

        elif choice == "2":

            view_payments()

        elif choice == "3":

            search_payment_by_booking()

        elif choice == "4":

            return

        else:

            print("\nInvalid choice.")