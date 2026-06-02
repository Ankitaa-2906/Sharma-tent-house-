from storage import load_data, save_data

CUSTOMER_FILE = "data/customers.json"


def generate_customer_id(customers):
    if not customers:
        return "C101"

    last_number = max(
        int(customer["customer_id"].replace("C", ""))
        for customer in customers
    )

    return f"C{last_number + 1}"


def add_customer():
    data = load_data(CUSTOMER_FILE)

    customers = data.get("customers", [])

    customer_id = generate_customer_id(customers)

    print(f"\nGenerated Customer ID: {customer_id}")

    customer_name = input("Enter Customer Name: ").strip()
    phone_number = input("Enter Phone Number: ").strip()
    address = input("Enter Address: ").strip()

    new_customer = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "phone_number": phone_number,
        "address": address
    }

    customers.append(new_customer)

    data["customers"] = customers

    save_data(CUSTOMER_FILE, data)

    print("\nCustomer added successfully.\n")


def view_customers():
    data = load_data(CUSTOMER_FILE)

    customers = data.get("customers", [])

    if not customers:
        print("\nNo customers found.\n")
        return

    print("\n===== CUSTOMERS =====\n")

    for customer in customers:
        print(f"Customer ID: {customer['customer_id']}")
        print(f"Name: {customer['customer_name']}")
        print(f"Phone: {customer['phone_number']}")
        print(f"Address: {customer['address']}")
        print("-" * 40)

    def find_customer():
     data = load_data(CUSTOMER_FILE)

    customers = data.get("customers", [])

    search = input("Enter customer name or phone number: "
 ).strip().lower()

    found = False

    for customer in customers:

        if (
            search in customer["customer_name"].lower()
            or search in customer["phone_number"]
        ):

            print(f"\nID: {customer['customer_id']}")
            print(f"Name: {customer['customer_name']}")
            print(f"Phone: {customer['phone_number']}")
            print("-" * 30)

            found = True

    if not found:
        print("\nNo matching customer found.\n")