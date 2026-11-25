
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MENU_FILE = os.path.join(BASE_DIR, "database", "menu.json")
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
        file.write(f"{datetime.now()} - {message}\n")


def save_error(message):
    errors = read_data(ERROR_FILE)

    errors.append({
        "error": message,
        "date": str(datetime.now())
    })

    save_data(ERROR_FILE, errors)


class Menu:

    def show_items(self, menu, item_type=None):
        found = False

        print("\n====================== MENU ITEMS ======================")
        print("{:<8} {:<23} {:<15} {:<12} {:<10}".format(
            "ID", "ITEM NAME", "CATEGORY", "TYPE", "PRICE"
        ))
        print("-" * 75)

        for item in menu:
            if item_type is None or item.get("item_type") == item_type:

                food_type = item.get("food_type", "-")

                print("{:<8} {:<23} {:<15} {:<12} Rs. {:<7}".format(
                    item.get("id", ""),
                    item.get("name", ""),
                    item.get("category", ""),
                    food_type,
                    item.get("price", 0)
                ))

                found = True

        if not found:
            print("No items found.")

        print("-" * 75)

        return found

    def add_item(self, item_type):

        while True:
            menu = read_data(MENU_FILE)

            print("\n======================", item_type.upper(), "ITEMS ======================")

            print("{:<8} {:<23} {:<15} {:<12} {:<10}".format(
                "ID", "ITEM NAME", "CATEGORY", "TYPE", "PRICE"
            ))

            print("-" * 75)

            found = False

            for item in menu:
                if item.get("item_type") == item_type:

                    food_type = item.get("food_type", "-")

                    print("{:<8} {:<23} {:<15} {:<12} Rs. {:<7}".format(
                        item.get("id", ""),
                        item.get("name", ""),
                        item.get("category", ""),
                        food_type,
                        item.get("price", 0)
                    ))

                    found = True

            if not found:
                print("No items found.")

            print("-" * 75)

            print("\n1. Add New", item_type, "Item")
            print("2. Back")

            choice = input("Enter choice: ")

            if choice == "2":
                return

            elif choice == "1":

                print("\n===== ADD NEW", item_type.upper(), "ITEM =====")

                name = input("Enter item name: ").strip()

                if not name:
                    print("Name cannot be empty.")
                    continue

                duplicate = False

                for item in menu:
                    if item.get("name", "").lower() == name.lower():
                        duplicate = True

                if duplicate:
                    print("Item already exists.")
                    continue

                category = input("Enter category: ").strip()

                if not category:
                    print("Category cannot be empty.")
                    continue

                try:
                    price = float(input("Enter price: "))

                    if price <= 0:
                        print("Price must be greater than zero.")
                        continue

                except ValueError:
                    print("Enter a valid price.")
                    continue

                food_type = ""

                if item_type == "Food":
                    food_type = input("Enter Veg or Non-Veg: ").strip().title()

                    if food_type not in ["Veg", "Non-Veg"]:
                        print("Invalid food type.")
                        continue

                next_id = 201

                for item in menu:
                    try:
                        next_id = max(next_id, int(item["id"]) + 1)
                    except (KeyError, ValueError, TypeError):
                        pass

                new_item = {
                    "id": str(next_id),
                    "name": name,
                    "category": category,
                    "price": int(price) if price.is_integer() else price,
                    "item_type": item_type,
                    "status": "Available",
                    "date": str(datetime.now())
                }

                if item_type == "Food":
                    new_item["food_type"] = food_type

                menu.append(new_item)

                save_data(MENU_FILE, menu)
                write_log(f"{item_type} added: {name}")

                print("\nItem added successfully!")
                print("Item ID:", next_id)

                return

            else:
                print("Invalid choice.")

    def view_menu(self, item_type=None):

        menu = read_data(MENU_FILE)

        self.show_items(menu, item_type)

        print("\n1. Back")
        input("Press Enter to go back...")

    def update_item(self):

        menu = read_data(MENU_FILE)

        self.show_items(menu)

        item_id = input("\nEnter item ID to update: ")

        for item in menu:

            if item.get("id") == item_id:

                print("\n1. Update Name")
                print("2. Update Category")
                print("3. Update Price")
                print("4. Update Status")

                choice = input("Enter choice: ")

                if choice == "1":
                    item["name"] = input("Enter new name: ")

                elif choice == "2":
                    item["category"] = input("Enter new category: ")

                elif choice == "3":
                    try:
                        price = float(input("Enter new price: "))

                        if price <= 0:
                            print("Invalid price.")
                            return

                        item["price"] = int(price) if price.is_integer() else price

                    except ValueError:
                        print("Invalid price.")
                        return

                elif choice == "4":

                    status = input("Enter Available or Unavailable: ").title()

                    if status not in ["Available", "Unavailable"]:
                        print("Invalid status.")
                        return

                    item["status"] = status

                else:
                    print("Invalid choice.")
                    return

                save_data(MENU_FILE, menu)

                write_log(f"Menu item updated: {item_id}")

                print("Item updated successfully.")
                return

        print("Item not found.")

    def delete_item(self):

        menu = read_data(MENU_FILE)

        self.show_items(menu)

        item_id = input("\nEnter item ID to delete: ")

        for item in menu:

            if item.get("id") == item_id:

                menu.remove(item)

                save_data(MENU_FILE, menu)

                write_log(f"Menu item deleted: {item_id}")

                print("Item deleted successfully.")
                return

        print("Item not found.")

    def search_item(self):

        menu = read_data(MENU_FILE)

        name = input("Enter item name to search: ").lower()

        found = False

        for item in menu:

            if name in item.get("name", "").lower():

                print("\nID:", item.get("id"))
                print("Name:", item.get("name"))
                print("Category:", item.get("category"))
                print("Price: Rs.", item.get("price"))
                print("Type:", item.get("item_type"))

                found = True

        if not found:
            print("Item not found.")


class MenuDisplay:

    def start(self):

        menu = Menu()

        while True:

            print("\n========== MENU MANAGEMENT ==========")
            print("1. Add Food Item")
            print("2. Add Drink Item")
            print("3. View Complete Menu")
            print("4. View Food Menu")
            print("5. View Drink Menu")
            print("6. Update Menu Item")
            print("7. Delete Menu Item")
            print("8. Search Menu Item")
            print("9. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                menu.add_item("Food")

            elif choice == "2":
                menu.add_item("Drink")

            elif choice == "3":
                menu.view_menu()

            elif choice == "4":
                menu.view_menu("Food")

            elif choice == "5":
                menu.view_menu("Drink")

            elif choice == "6":
                menu.update_item()

            elif choice == "7":
                menu.delete_item()

            elif choice == "8":
                menu.search_item()

            elif choice == "9":
                break

            else:
                print("Invalid choice.")


if __name__ == "__main__":
    MenuDisplay().start()