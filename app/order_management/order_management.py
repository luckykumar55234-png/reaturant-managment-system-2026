
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MENU_FILE = os.path.join(BASE_DIR, "database", "menu.json")
ORDER_FILE = os.path.join(BASE_DIR, "database", "orders.json")
LOG_FILE = os.path.join(BASE_DIR, "logs", "royal_plate.log")
ERROR_FILE = os.path.join(BASE_DIR, "errors", "errors.json")


def read_data(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

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


class OrderManagement:

    def __init__(self):
        self.menu = self.load_menu()

    def load_menu(self):

        menu = read_data(MENU_FILE)

        default_items = [

            # Pizza
            ("Margherita Pizza", 199, "Pizza", "Veg"),
            ("Cheese Pizza", 249, "Pizza", "Veg"),
            ("Paneer Pizza", 279, "Pizza", "Veg"),
            ("Farmhouse Pizza", 299, "Pizza", "Veg"),

            # Fast Food
            ("Veg Burger", 99, "Fast Food", "Veg"),
            ("Cheese Burger", 149, "Fast Food", "Veg"),
            ("French Fries", 89, "Fast Food", "Veg"),
            ("Garlic Bread", 110, "Fast Food", "Veg"),
            ("Veg Sandwich", 100, "Fast Food", "Veg"),
            ("Cheese Sandwich", 130, "Fast Food", "Veg"),

            # Indian Food
            ("Veg Biryani", 180, "Indian Food", "Veg"),
            ("Chicken Biryani", 250, "Indian Food", "Non-Veg"),
            ("Paneer Biryani", 220, "Indian Food", "Veg"),
            ("Dal Makhani", 180, "Indian Food", "Veg"),
            ("Paneer Tikka", 220, "Indian Food", "Veg"),
            ("Veg Thali", 180, "Indian Food", "Veg"),
            ("Butter Naan", 40, "Indian Food", "Veg"),
            ("Chole Bhature", 130, "Indian Food", "Veg"),
            ("Shahi Paneer", 210, "Indian Food", "Veg"),
            ("Jeera Rice", 120, "Indian Food", "Veg"),

            # Chinese
            ("Veg Chowmein", 100, "Chinese", "Veg"),
            ("Hakka Noodles", 130, "Chinese", "Veg"),
            ("Veg Manchurian", 140, "Chinese", "Veg"),
            ("Fried Rice", 130, "Chinese", "Veg"),
            ("Chilli Paneer", 180, "Chinese", "Veg"),

            # Snacks
            ("Samosa", 25, "Snacks", "Veg"),
            ("Aloo Tikki", 50, "Snacks", "Veg"),
            ("Spring Roll", 120, "Snacks", "Veg"),
            ("Cheese Balls", 100, "Snacks", "Veg"),

            # Drinks
            ("American Cold Coffee", 120, "Drinks", ""),
            ("Coca Cola", 50, "Drinks", ""),
            ("Pepsi", 50, "Drinks", ""),
            ("Sprite", 50, "Drinks", ""),
            ("Lemon Soda", 60, "Drinks", ""),
            ("Chocolate Milkshake", 130, "Drinks", ""),
            ("Vanilla Milkshake", 120, "Drinks", ""),
            ("Mineral Water", 30, "Drinks", ""),
            ("Mojito", 100, "Drinks", ""),
            ("Fresh Lime Juice", 80, "Drinks", ""),

            # Desserts
            ("Chocolate Brownie", 120, "Desserts", "Veg"),
            ("Vanilla Ice Cream", 80, "Desserts", "Veg"),
            ("Gulab Jamun", 70, "Desserts", "Veg")
        ]

        existing_names = []

        for item in menu:
            existing_names.append(item.get("name", "").lower())

        next_id = 201

        for item in menu:
            try:
                item_id = int(item.get("id", 0))

                if item_id >= next_id:
                    next_id = item_id + 1

            except (ValueError, TypeError):
                pass

        for name, price, category, food_type in default_items:

            if name.lower() not in existing_names:

                if category == "Drinks":
                    item_type = "Drink"
                else:
                    item_type = "Food"

                new_item = {
                    "id": str(next_id),
                    "name": name,
                    "category": category,
                    "item_type": item_type,
                    "price": price,
                    "status": "Available",
                    "date": str(datetime.now().date()),
                    "time": datetime.now().strftime("%H:%M:%S")
                }

                if food_type:
                    new_item["food_type"] = food_type

                menu.append(new_item)
                existing_names.append(name.lower())
                next_id += 1

        for item in menu:

            if item.get("item_type") == "Drink":
                item.pop("food_type", None)

        save_data(MENU_FILE, menu)

        return menu

    def show_menu(self):

        self.menu = self.load_menu()

        print("\n" + "=" * 65)
        print("                  THE ROYAL PLATE")
        print("                  RESTAURANT MENU")
        print("=" * 65)

        available_items = []

        for item in self.menu:

            if item.get("status", "Available") == "Available":
                available_items.append(item)

        if not available_items:
            print("No Menu Items Available!")
            return

        categories = []

        for item in available_items:

            category = item.get("category", "Other")

            if category not in categories:
                categories.append(category)

        for category in categories:

            print("\n" + "-" * 65)
            print("                    " + category.upper())
            print("-" * 65)

            if category == "Drinks":
                print("{:<8} {:<40} {:>10}".format(
                    "ID", "DRINK NAME", "PRICE"
                ))
            else:
                print("{:<8} {:<30} {:<12} {:>8}".format(
                    "ID", "ITEM NAME", "TYPE", "PRICE"
                ))

            for item in available_items:

                if item.get("category", "Other") == category:

                    if category == "Drinks":

                        print("{:<8} {:<40} Rs.{:>7}".format(
                            str(item.get("id", "")),
                            item.get("name", ""),
                            item.get("price", 0)
                        ))

                    else:

                        print("{:<8} {:<30} {:<12} Rs.{:>5}".format(
                            str(item.get("id", "")),
                            item.get("name", ""),
                            item.get("food_type", ""),
                            item.get("price", 0)
                        ))

        print("\n" + "=" * 65)

    def create_order(self):

        orders = read_data(ORDER_FILE)

        print("\n===== CREATE NEW ORDER =====")

        customer_name = input("Enter Customer Name: ")

        if customer_name == "" or not customer_name.replace(" ", "").isalpha():
            print("Invalid Customer Name!")
            save_error("Invalid customer name")
            return

        phone = input("Enter Phone Number: ")

        if len(phone) != 10 or not phone.isdigit():
            print("Phone Number must be 10 digits!")
            save_error("Invalid phone number")
            return

        print("\n1. Dine In")
        print("2. Takeaway")
        print("3. Delivery")

        choice = input("Select Order Type: ")

        if choice == "1":
            order_type = "Dine In"
        elif choice == "2":
            order_type = "Takeaway"
        elif choice == "3":
            order_type = "Delivery"
        else:
            print("Invalid Order Type!")
            save_error("Invalid order type")
            return

        address = ""

        if order_type == "Delivery":

            address = input("Enter Delivery Address: ")

            if address == "":
                print("Address is required!")
                save_error("Delivery address missing")
                return

        self.show_menu()
        self.menu = self.load_menu()

        selected_items = []
        total = 0

        while True:

            item_id = input("\nEnter Item ID: ")

            selected_item = None

            for item in self.menu:

                if str(item.get("id", "")) == item_id:

                    if item.get("status", "Available") == "Available":
                        selected_item = item

                    break

            if selected_item is None:
                print("Item Not Found or Not Available!")
                save_error("Invalid item ID")
                continue

            try:
                quantity = int(input("Enter Quantity: "))

                if quantity <= 0:
                    print("Quantity must be greater than zero!")
                    continue

            except ValueError:
                print("Enter a valid quantity!")
                save_error("Invalid quantity")
                continue

            price = float(selected_item.get("price", 0))

            if price.is_integer():
                price = int(price)

            amount = price * quantity

            order_item = {
                "id": str(selected_item["id"]),
                "name": selected_item["name"],
                "price": price,
                "quantity": quantity,
                "amount": amount
            }

            selected_items.append(order_item)
            total += amount

            print(selected_item["name"], "Added Successfully!")
            print("Item Amount: Rs.", amount)

            while True:

                again = input("\nDo you want to add another item? (Yes/No): ").lower()

                if again == "yes":
                    break

                elif again == "no":
                    break

                else:
                    print("Please enter Yes or No.")

            if again == "no":
                break

        if not selected_items:
            print("No Items Selected!")
            return

        order_id = str(int(datetime.now().timestamp()))

        order = {
            "id": order_id,
            "customer_name": customer_name,
            "customer_phone": phone,
            "order_type": order_type,
            "address": address,
            "items": selected_items,
            "total": total,
            "status": "Active",
            "date": str(datetime.now().date()),
            "time": datetime.now().strftime("%H:%M:%S")
        }

        orders.append(order)
        save_data(ORDER_FILE, orders)

        write_log("New order created: " + order_id)

        print("\n" + "=" * 45)
        print("           ORDER SUCCESSFUL")
        print("=" * 45)

        print("Order ID:", order_id)
        print("Customer:", customer_name)
        print("Phone:", phone)
        print("Order Type:", order_type)

        print("-" * 45)

        for item in selected_items:
            print(item["name"])
            print("Quantity:", item["quantity"])
            print("Amount: Rs.", item["amount"])

        print("-" * 45)
        print("TOTAL AMOUNT: Rs.", total)
        print("Status: Active")
        print("Date:", order["date"])
        print("Time:", order["time"])
        print("=" * 45)

    def view_orders(self):

        orders = read_data(ORDER_FILE)

        print("\n===== ALL ORDERS =====")

        if not orders:
            print("No Orders Found!")
            return

        for order in orders:

            print("\n" + "=" * 45)

            print("Order ID:", order["id"])
            print("Customer:", order["customer_name"])
            print("Phone:", order["customer_phone"])
            print("Order Type:", order["order_type"])

            if order.get("address"):
                print("Address:", order["address"])

            print("-" * 45)

            for item in order["items"]:

                print(
                    item["name"],
                    "| Quantity:", item["quantity"],
                    "| Amount: Rs.",
                    item.get("amount", item["price"] * item["quantity"])
                )

            print("-" * 45)

            print("Total: Rs.", order["total"])
            print("Status:", order["status"])
            print("Date:", order["date"])
            print("Time:", order["time"])

        write_log("Orders viewed")

    def cancel_order(self):

        orders = read_data(ORDER_FILE)

        print("\n===== CANCEL ORDER =====")

        order_id = input("Enter Order ID: ")

        if not order_id.isdigit():
            print("Invalid Order ID!")
            save_error("Invalid order ID")
            return

        for order in orders:

            if order["id"] == order_id:

                if order["status"] != "Active":
                    print("Order cannot be cancelled!")
                    return

                order["status"] = "Cancelled"

                save_data(ORDER_FILE, orders)
                write_log("Order cancelled: " + order_id)

                print("Order Cancelled Successfully!")
                return

        print("Order Not Found!")
        save_error("Order not found during cancellation")


class OrderMenu:

    def start(self):

        order = OrderManagement()

        while True:

            print("\n" + "=" * 40)
            print("          ORDER MANAGEMENT")
            print("           THE ROYAL PLATE")
            print("=" * 40)

            print("1. Show Food Menu")
            print("2. Create Order")
            print("3. View Orders")
            print("4. Cancel Order")
            print("5. Back to Main Menu")

            print("=" * 40)

            choice = input("Enter Choice: ")

            if choice == "1":
                order.show_menu()

            elif choice == "2":
                order.create_order()

            elif choice == "3":
                order.view_orders()

            elif choice == "4":
                order.cancel_order()

            elif choice == "5":
                break

            else:
                print("Invalid Choice!")


if __name__ == "__main__":
    OrderMenu().start()
