from storage import load_data

PAYMENT_FILE = "payments.json"

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

        amount = float(payment.get("amount", 0))

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

def reports_menu():

    while True:

        print("\n===== REPORTS =====")

        print("1. Revenue Report")

        print("2. Back")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":

            revenue_report()

        elif choice == "2":

            break

        else:

            print("\nInvalid choice.")