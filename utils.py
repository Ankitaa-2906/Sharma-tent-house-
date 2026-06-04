from datetime import datetime


def read_date(prompt):
    while True:
        date_input = input(prompt).strip()

        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input

        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")