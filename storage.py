import json
import os


def load_data(file_path):
    """
    Loads data from a JSON file.
    """

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print(f"Error: {file_path} contains invalid JSON.")
        return {}


def save_data(file_path, data):
    """
    Saves data to a JSON file.
    """

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)