
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "database")


def read_data(file_path):

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (OSError, json.JSONDecodeError):
        return []


def save_data(file_path, data):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


class CalculateTotal:

    def __init__(self):

        self.order_file = os.path.join(DATA_DIR, "orders.json")
        self.bill_file = os.path.join(DATA_DIR, "bills.json")
        self.booking_file = os.path.join(DATA_DIR, "bookings.json")
        self.table_file = os.path.join(DATA_DIR, "tables.json")

        os.makedirs(DATA_DIR, exist_ok=True)

    def calculate(self, order_id):

        if len(order_id) != 10 or not order_id.isdigit():
            print("Order ID must be 10 digits.")
            return None

        orders = read_data(self.order_file)

        for order in orders:

            if order.get("id") == order_id:

                if order.get("status") != "Active":
                    print("Only active orders can be billed.")
                    return None

                total = 0

                for item in order.get("items", []):
                    price = item.get("price", 0)
                    quantity = item.get("quantity", 0)
                    total += price * quantity

                return total

        print("Order not found.")
        return None


class Tax(CalculateTotal):

    def calculate_tax(self, order_id):

        subtotal = self.calculate(order_id)

        if subtotal is None:
            return None

        gst = subtotal * 5 / 100
        total = subtotal + gst

        print("Subtotal:", round(subtotal, 2))
        print("GST 5%:", round(gst, 2))
        print("Total:", round(total, 2))

        return {
            "subtotal": round(subtotal, 2),
            "gst": round(gst, 2),
            "total": round(total, 2)
        }


class Discount(Tax):

    def calculate_discount(self, order_id):

        subtotal = self.calculate(order_id)

        if subtotal is None:
            return None

        try:
            discount_percent = float(input("Enter discount percentage: "))

            if discount_percent < 0 or discount_percent > 100:
                print("Discount must be between 0 and 100.")
                return None

        except ValueError:
            print("Please enter a valid number.")
            return None

        discount = subtotal * discount_percent / 100
        amount = subtotal - discount
        gst = amount * 5 / 100
        total = amount + gst

        print("\nSubtotal:", round(subtotal, 2))
        print("Discount:", round(discount, 2))
        print("After Discount:", round(amount, 2))
        print("GST 5%:", round(gst, 2))
        print("Final Total:", round(total, 2))

        return {
            "subtotal": round(subtotal, 2),
            "discount_percent": discount_percent,
            "discount": round(discount, 2),
            "after_discount": round(amount, 2),
            "gst": round(gst, 2),
            "total": round(total, 2)
        }


class GenerateBill(Discount):

    def generate_bill(self, order_id):

        print("\n========== THE ROYAL PLATE ==========")

        if len(order_id) != 10 or not order_id.isdigit():
            print("Order ID must be 10 digits.")
            return

        orders = read_data(self.order_file)
        selected_order = None

        for order in orders:

            if order.get("id") == order_id:
                selected_order = order
                break

        if selected_order is None:
            print("Order not found.")
            return

        if selected_order.get("status") != "Active":
            print("This order is already completed or inactive.")
            return

        result = self.calculate_discount(order_id)

        if result is None:
            return

        payment = input("Payment (Cash/Card/Online): ")

        if payment.lower() not in ["cash", "card", "online"]:
            print("Please select Cash, Card, or Online.")
            return

        bills = read_data(self.bill_file)
        bill_id = str(4000000000 + len(bills) + 1)

        items = []

        for item in selected_order.get("items", []):

            new_item = item.copy()
            new_item["line_total"] = (
                item.get("price", 0) * item.get("quantity", 0)
            )

            items.append(new_item)

        booking_id = selected_order.get("booking_id")
        table_id = selected_order.get("table_id")

        bill = {
            "id": bill_id,
            "order_id": order_id,
            "order_type": selected_order.get("order_type", "Not recorded"),
            "booking_id": booking_id,
            "table_id": table_id,
            "customer_name": selected_order.get("customer_name"),
            "customer_phone": selected_order.get("customer_phone"),
            "people": selected_order.get("people"),
            "items": items,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subtotal": result["subtotal"],
            "discount_percent": result["discount_percent"],
            "discount": result["discount"],
            "gst": result["gst"],
            "total": result["total"],
            "payment": payment.title()
        }

        bills.append(bill)
        save_data(self.bill_file, bills)

        selected_order["status"] = "Complete"
        save_data(self.order_file, orders)

        # Booking complete aur table available karna
        if booking_id:

            bookings = read_data(self.booking_file)

            for booking in bookings:

                if str(booking.get("id")) == str(booking_id):

                    booking["status"] = "Complete"
                    table_id = booking.get("table_id", table_id)

                    save_data(self.booking_file, bookings)

                    tables = read_data(self.table_file)

                    for table in tables:

                        if str(table.get("id")) == str(table_id):

                            table["status"] = "Available"
                            save_data(self.table_file, tables)
                            break

                    break

        print("\n========== THE ROYAL PLATE BILL ==========")
        print("Bill ID:", bill_id)
        print("Order ID:", order_id)
        print("Customer:", selected_order.get("customer_name"))
        print("Date:", bill["date"])

        print("\nItems:")

        for item in items:

            name = item.get("name", "Unknown")
            quantity = item.get("quantity", 0)
            price = item.get("price", 0)
            line_total = item.get("line_total", 0)

            print(name, "| Qty:", quantity,
                  "| Price:", price, "| Total:", line_total)

        print("\nSubtotal:", result["subtotal"])
        print("Discount:", result["discount"])
        print("GST 5%:", result["gst"])
        print("Final Total:", result["total"])
        print("Payment:", payment.title())
        print("Bill generated successfully.")


class BillingMenu:

    def start(self):

        billing = GenerateBill()

        while True:

            print("\n===== BILLING MANAGEMENT =====")
            print("1. Generate Bill")
            print("2. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":

                order_id = input("Enter 10 Digit Order ID: ")
                billing.generate_bill(order_id)

            elif choice == "2":
                break

            else:
                print("Invalid Choice.")


if __name__ == "__main__":
    BillingMenu().start()