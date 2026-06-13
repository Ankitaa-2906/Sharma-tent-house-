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

    while True:
        customer_name = input(
            "Enter Customer Name: "
        ).strip()

        if customer_name:
            break

        print("Customer name cannot be empty.")


    while True:

        phone_number = input(
            "Enter Phone Number: "
        ).strip()

        if not phone_number:
            print("Phone number cannot be empty.")
            continue

        if not phone_number.isdigit():
            print("Phone number must contain digits only.")
            continue

        if len(phone_number) != 10:
            print("Phone number must be exactly 10 digits.")
            continue

        if any(
            customer["phone_number"] == phone_number
            for customer in customers
        ):
            print(
                "\nPhone number already exists.\n"
            )
            continue

        break

    while True:
        address = input(
            "Enter Address: "
        ).strip()

        if address:
            break

        print("Address cannot be empty.")

    new_customer = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "phone_number": phone_number,
        "address": address
    }

    customers.append(new_customer)

    data["customers"] = customers

    save_data(CUSTOMER_FILE, data)

    print("\n===== CUSTOMER SUMMARY =====")

    print(
        f"Customer ID : "
        f"{customer_id}"
    )

    print(
        f"Name        : "
        f"{customer_name}"
    )

    print(
        f"Phone       : "
        f"{phone_number}"
    )

    print(
        f"Address     : "
        f"{address}"
    )

    print(
        "\nCustomer added successfully."
    )


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
    search = input(
        "Enter customer name or phone: "
    ).strip().lower()

    data = load_data(CUSTOMER_FILE)
    customers = data.get("customers", [])

    matches = []

    for customer in customers:
        if (
            search in customer["customer_name"].lower()
            or search in customer["phone_number"]
        ):
            matches.append(customer)

    if not matches:
        print("\nCustomer not found.")
        return None

    print("\nMatching Customers:")

    for index, customer in enumerate(matches, start=1):
        print(
            f"{index}. "
            f"{customer['customer_id']} | "
            f"{customer['customer_name']} | "
            f"{customer['phone_number']}"
        )

    try:
        choice = int(
            input("\nSelect customer number: ")
        )

        if 1 <= choice <= len(matches):
            return matches[choice - 1]["customer_id"]

    except ValueError:
        pass

    print("Invalid selection.")
    return None

def update_customer():

    data = load_data(CUSTOMER_FILE)

    customers = data.get(
        "customers",
        []
    )

    customer_id = find_customer()

    if customer_id is None:
        return

    customer_found = None

    for customer in customers:

        if customer["customer_id"] == customer_id:

            customer_found = customer
            break

    if customer_found is None:

        print(
            "\nCustomer not found."
        )

        return

    while True:

        print("\n===== UPDATE CUSTOMER =====")

        print("1. Update Name")
        print("2. Update Phone Number")
        print("3. Update Address")
        print("4. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            while True:

                new_name = input(
                    "Enter New Name: "
                ).strip()

                if not new_name:

                    print(
                        "Name cannot be empty."
                    )

                    continue

                customer_found[
                    "customer_name"
                ] = new_name.title()

                save_data(
                    CUSTOMER_FILE,
                    data
                )

                print(
                    "\nName updated successfully."
                )

                break

        elif choice == "2":

            while True:

                new_phone = input(
                    "Enter New Phone Number: "
                ).strip()

                if not new_phone.isdigit():

                    print(
                        "Phone number must contain digits only."
                    )

                    continue

                if len(new_phone) != 10:

                    print(
                        "Phone number must be exactly 10 digits."
                    )

                    continue

                phone_exists = False

                for customer in customers:

                    if (
                        customer["phone_number"]
                        == new_phone
                        and
                        customer["customer_id"]
                        != customer_found["customer_id"]
                    ):

                        phone_exists = True
                        break

                if phone_exists:

                    print(
                        "Phone number already exists."
                    )

                    continue

                customer_found[
                    "phone_number"
                ] = new_phone

                save_data(
                    CUSTOMER_FILE,
                    data
                )

                print(
                    "\nPhone number updated successfully."
                )

                break

        elif choice == "3":

            while True:

                new_address = input(
                    "Enter New Address: "
                ).strip()

                if not new_address:

                    print(
                        "Address cannot be empty."
                    )

                    continue

                customer_found[
                    "address"
                ] = new_address

                save_data(
                    CUSTOMER_FILE,
                    data
                )

                print(
                    "\nAddress updated successfully."
                )

                break

        elif choice == "4":

            print("\nReturning to Customer Menu...")

            return

        else:

            print(
                "\nInvalid choice."
            )
def customer_menu():

    while True:

        print("\n===== CUSTOMER MANAGEMENT =====")

        print("1. Add Customer")
        print("2. View Customers")
        print("3. Find Customer")
        print("4. Update Customer")
        print("5. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            add_customer()

        elif choice == "2":

            view_customers()

        elif choice == "3":

            find_customer()

        elif choice == "4":

            update_customer()

        elif choice == "5":

            return

        else:

            print("\nInvalid choice.")