
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INVENTORY_FILE = os.path.join(BASE_DIR, "database", "inventory.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "royal_plate.log")
ERROR_FILE = os.path.join(BASE_DIR, "errors", "errors.json")


def read_data(file_path):

    try:
        with open(file_path, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(file_path, data):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def write_log(message):

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a") as file:
        file.write(str(datetime.now()) + " - " + message + "\n")


def save_error(message):

    errors = read_data(ERROR_FILE)

    errors.append({
        "error": message,
        "date": str(datetime.now())
    })

    save_data(ERROR_FILE, errors)


class Inventory:

    def add_item(self):

        items = read_data(INVENTORY_FILE)

        print("\n===== ADD INVENTORY ITEM =====")

        item_id = input("Enter Item ID: ")
        name = input("Enter Item Name: ")

        if not item_id.isdigit():
            print("Item ID must contain numbers.")
            save_error("Invalid inventory item ID")
            return

        if not name.replace(" ", "").isalpha():
            print("Enter a valid item name.")
            save_error("Invalid inventory item name")
            return

        for item in items:
            if item["id"] == item_id:
                print("Item ID already exists.")
                save_error("Duplicate inventory item ID")
                return

        try:
            quantity = int(input("Enter Quantity: "))
            price = float(input("Enter Price: "))

            if quantity <= 0 or price <= 0:
                print("Quantity and price must be greater than zero.")
                save_error("Invalid inventory quantity or price")
                return

        except ValueError:
            print("Please enter valid numbers.")
            save_error("Invalid inventory input")
            return

        item = {
            "id": item_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "date": str(datetime.now().date()),
            "time": str(datetime.now().time())
        }

        items.append(item)
        save_data(INVENTORY_FILE, items)

        write_log("Inventory item added: " + name)

        print("Item Added Successfully!")

    def view_items(self):

        items = read_data(INVENTORY_FILE)

        print("\n===== INVENTORY ITEMS =====")

        if not items:
            print("No inventory items found.")
            return

        for item in items:

            print("-------------------------")
            print("Item ID:", item["id"])
            print("Name:", item["name"])
            print("Quantity:", item["quantity"])
            print("Price:", item["price"])
            print("Date:", item["date"])
            print("Time:", item["time"])

        write_log("Inventory items viewed")

    def update_item(self):

        items = read_data(INVENTORY_FILE)

        print("\n===== UPDATE INVENTORY =====")

        item_id = input("Enter Item ID: ")

        for item in items:

            if item["id"] == item_id:

                try:
                    quantity = int(input("Enter New Quantity: "))
                    price = float(input("Enter New Price: "))

                    if quantity <= 0 or price <= 0:
                        print("Values must be greater than zero.")
                        save_error("Invalid inventory update values")
                        return

                except ValueError:
                    print("Enter valid numbers.")
                    save_error("Invalid inventory update input")
                    return

                item["quantity"] = quantity
                item["price"] = price
                item["date"] = str(datetime.now().date())
                item["time"] = str(datetime.now().time())

                save_data(INVENTORY_FILE, items)

                write_log("Inventory item updated: " + item_id)

                print("Item Updated Successfully!")
                return

        print("Item Not Found.")
        save_error("Inventory item not found during update")

    def delete_item(self):

        items = read_data(INVENTORY_FILE)

        print("\n===== DELETE INVENTORY ITEM =====")

        item_id = input("Enter Item ID: ")

        for item in items:

            if item["id"] == item_id:

                items.remove(item)
                save_data(INVENTORY_FILE, items)

                write_log("Inventory item deleted: " + item_id)

                print("Item Deleted Successfully!")
                return

        print("Item Not Found.")
        save_error("Inventory item not found during delete")


class InventoryMenu:

    def start(self):

        inventory = Inventory()

        while True:

            print("\n===== INVENTORY MANAGEMENT =====")
            print("1. Add Item")
            print("2. View Items")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                inventory.add_item()

            elif choice == "2":
                inventory.view_items()

            elif choice == "3":
                inventory.update_item()

            elif choice == "4":
                inventory.delete_item()

            elif choice == "5":
                break

            else:
                print("Invalid Choice.")


if __name__ == "__main__":
    InventoryMenu().start()
