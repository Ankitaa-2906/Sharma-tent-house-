import datetime

from inventory_service import INVENTORY_FILE
from storage import load_data, save_data

BOOKING_FILE = "data/bookings.json"
RETURN_FILE = "data/returns.json"


def get_inventory_item(item_id):

    inventory_data = load_data(
        INVENTORY_FILE
    )

    inventory = inventory_data.get(
        "inventory_items",
        []
    )

    for item in inventory:

        if item["item_id"] == item_id:

            return item

    return None


def find_booking():

    booking_data = load_data(
        BOOKING_FILE
    )

    bookings = booking_data.get(
        "bookings",
        []
    )

    search = input(
        "\nEnter Booking ID or Event Name: "
    ).strip().lower()

    matches = []

    for booking in bookings:

        if (
            search in booking["booking_id"].lower()
            or search in booking["event_name"].lower()
        ):

            matches.append(
                booking
            )

    if not matches:

        print(
            "\nNo matching booking found."
        )

        return None

    print(
        "\n===== MATCHING BOOKINGS ====="
    )

    for index, booking in enumerate(
        matches,
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
            len(matches)
        ):

            return matches[
                choice - 1
            ]

    except ValueError:

        pass

    print(
        "\nInvalid selection."
    )

    return None


def record_return():

    booking_data = load_data(
        BOOKING_FILE
    )

    return_data = load_data(
        RETURN_FILE
    )

    returns = return_data.get(
        "returns",
        []
    )

    print(
        "\nSearch Booking"
    )

    booking_found = find_booking()

    if booking_found is None:

        return

    booking_id = booking_found[
        "booking_id"
    ]

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

        inventory_item = get_inventory_item(
            item["item_id"]
        )

        damage_charge = (
            damaged_quantity *
            inventory_item.get(
                "damage_charge",
                0
            )
        )

        missing_charge = (
            missing_quantity *
            inventory_item.get(
                "replacement_cost",
                0
            )
        )

        total_charge = (
            damage_charge +
            missing_charge
        )

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
            damaged_quantity,

            "damage_charge":
            damage_charge,

            "missing_charge":
            missing_charge,

            "total_charge":
            total_charge

        })

    return_record = {

        "booking_id":
        booking_id,

        "return_date":
        datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "return_status":
        "completed",

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

    grand_total = 0

    for item in returned_items:

        print(
            f"\nItem: "
            f"{item['item_id']}"
        )

        print(
            f"Returned: "
            f"{item['returned_quantity']}"
        )

        print(
            f"Missing: "
            f"{item['missing_quantity']}"
        )

        print(
            f"Damaged: "
            f"{item['damaged_quantity']}"
        )

        print(
            f"Damage Charge: ₹"
            f"{item['damage_charge']}"
        )

        print(
            f"Missing Charge: ₹"
            f"{item['missing_charge']}"
        )

        print(
            f"Total Charge: ₹"
            f"{item['total_charge']}"
        )

        grand_total += (
            item["total_charge"]
        )

    print(
        f"\nGrand Total Charge: ₹{grand_total}"
    )


def view_returns():

    data = load_data(
        RETURN_FILE
    )

    returns = data.get(
        "returns",
        []
    )

    if not returns:

        print(
            "\nNo returns found."
        )

        return

    for record in returns:

        print(
            f"\nBooking ID: "
            f"{record['booking_id']}"
        )

        print(
            f"Date: "
            f"{record['return_date']}"
        )

        print(
            f"Status: "
            f"{record['return_status']}"
        )

        print(
            "-" * 40
        )


def return_menu():

    while True:

        print(
            "\n===== RETURN MANAGEMENT ====="
        )

        print(
            "1. Record Return"
        )

        print(
            "2. View Returns"
        )

        print(
            "3. Back"
        )

        choice = input(
            "\nEnter Choice: "
        ).strip()

        if choice == "1":

            record_return()

        elif choice == "2":

            view_returns()

        elif choice == "3":

            return

        else:

            print(
                "\nInvalid choice."
            )