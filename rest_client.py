#!/usr/bin/env python3

"""

Rest API client - 2020, Nien Huei Chang

rest_client.py - client

"""

import requests


def list_records():
    """ List the names associated with all records. Key 'name' is the unique record identifier """

    response = requests.get("http://localhost:5000/api/names")

    print()
    for name in response.json():
        print(name)
    print()


def add_record():
    """ Add new record, 'name' key is required, other keys are optional """

    name = input("Enter a name to add your record (empty to cancel): ")
    print()

    if not name:
        return

    record = {"name": name}

    while True:
        key = input(f"Enter a key to be added to {name}'s record (empty to cancel): ")
        print()

        if not key:
            break

        while True:
            value = input(f"Enter the value for key '{key.lower()}': ")
            print()

            if not value:
                print("Value cannot be empty.")
                print()
                continue

            record[f"{key.lower()}"] = value
            break

    response = requests.post("http://localhost:5000/api/names", json=record)

    if response.status_code != 200:
        print(response.json()["message"])

    print()
    print(f"{name}'s record has been successfully added to database.")
    print()


def display_record():
    """ Display record by name """

    name = input("Enter a name to display the record (empty to cancel): ")
    print()

    if not name:
        return

    response = requests.get(f"http://localhost:5000/api/names/{name}")

    if response.status_code != 200:
        print()
        print(response.json()["message"])
        print()
        return

    print()
    for key, value in response.json().items():
        print(f"{key}: {value}")
    print()


def update_record():
    """ Select record by name and update with provided keys; empty key value removes key """

    record = {}

    name = input("Enter a name to update the associated record (empty to cancel): ")
    print()

    if not name:
        return

    if name not in requests.get("http://localhost:5000/api/names").json():
        print(f"{name}'s record does not exist in database")
        return

    while True:
        key = input(f"Enter a key to be modified or updated in {name}'s record (empty to cancel): ")
        print()

        if not key:
            break

        while True:
            value = input(f"Enter the value for key '{key}', empty to delete the key: ")
            print()
            record[f"{key.lower()}"] = value
            break

    response = requests.put(f"http://localhost:5000/api/names/{name}", json=record)

    if response.status_code != 200:
        print(response.json()["message"])

    print()
    print(f"{name}'s record has been updated successfully.")
    print()


def delete_record():
    """ Delete record by name """

    print()
    name = input("Enter a name to delete the associated record (empty to cancel): ")
    print()

    if not name:
        return

    response = requests.delete(f"http://localhost:5000/api/names/{name}")

    if response.status_code != 200:
        print()
        print(response.json()["message"])
        print()
        return

    print()
    print(f"{name}'s record has been successfully deleted.")
    print()


def main():
    """ Display main menu and wait for user to take action """

    while True:
        print()
        print("----------------- Menu ------------------")
        print(" 1 - Display a list of all names")
        print(" 2 - Add a record")
        print(" 3 - Display a record by name")
        print(" 4 - Update content of a specific record")
        print(" 5 - Delete a record by name")
        print(" 0 - Exit")
        print("-----------------------------------------")
        print()
        user_input = input("Press 0-5 to choose your option: ")
        print()

        if user_input == "1":
            list_records()

        elif user_input == "2":
            add_record()

        elif user_input == "3":
            display_record()

        elif user_input == "4":
            update_record()

        elif user_input == "5":
            delete_record()

        elif user_input == "0":
            break

        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()
