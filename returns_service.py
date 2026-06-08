from storage import load_data, save_data

BOOKING_FILE = "data/bookings.json"
RETURN_FILE = "data/returns.json"

def record_return():
    booking_data = load_data(
        BOOKING_FILE
    )

    return_data = load_data(
        RETURN_FILE
    )

    bookings = booking_data.get(
        "bookings",
        []
    )

    returns = return_data.get(
        "returns",
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

    returned_items = []

    print(
        "\n===== RETURN ITEMS ====="
    )

    for item in booking_found["items"]:

        booked_quantity = item["quantity"]

        print(
            f"\nItem: {item['item_id']}"
        )

        print(
            f"Booked Quantity: "
            f"{booked_quantity}"
        )

        try:

            returned_quantity = int(
                input(
                    "Returned Quantity: "
                )
            )

        except ValueError:

            print(
                "Invalid quantity."
            )

            return

        if (
            returned_quantity < 0
            or
            returned_quantity > booked_quantity
        ):

            print(
                "Returned quantity invalid."
            )

            return

        missing_quantity = (
            booked_quantity
            - returned_quantity
        )

        print(
            f"Missing Quantity: "
            f"{missing_quantity}"
        )

        damaged_quantity = 0

        if returned_quantity > 0:

            try:

                damaged_quantity = int(
                    input(
                        "Damaged Quantity: "
                    )
                )

            except ValueError:

                print(
                    "Invalid quantity."
                )

                return

            if (
                damaged_quantity < 0
                or
                damaged_quantity > returned_quantity
            ):

                print(
                    "Damaged quantity invalid."
                )

                return

        returned_items.append({

            "item_id":
            item["item_id"],

            "booked_quantity":
            booked_quantity,

            "returned_quantity":
            returned_quantity,

            "missing_quantity":
            missing_quantity,

            "damaged_quantity":
            damaged_quantity

        })

    return_record = {

        "booking_id":
        booking_id,

        "returned_items":
        returned_items

    }

    returns.append(
        return_record
    )

    return_data["returns"] = returns

    save_data(
        RETURN_FILE,
        return_data
    )

    print(
        "\nReturn recorded successfully."
    )

    print(
        "\n===== RETURN SUMMARY ====="
    )

    for item in returned_items:

        print(

            f"{item['item_id']} | "

            f"Returned: "
            f"{item['returned_quantity']} | "

            f"Missing: "
            f"{item['missing_quantity']} | "

            f"Damaged: "
            f"{item['damaged_quantity']}"

        )

def return_menu():

    while True:

        print("\n===== RETURN MANAGEMENT =====")

        print("1. Record Return")
        print("0. Back")

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            record_return()

        elif choice == "0":

            return

        else:

            print("\nInvalid choice.")