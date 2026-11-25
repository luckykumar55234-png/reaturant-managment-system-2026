
import json
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TABLE_FILE = os.path.join(BASE_DIR, "database", "tables.json")
BOOKING_FILE = os.path.join(BASE_DIR, "database", "bookings.json")
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
        file.write(f"{datetime.now()} - {message}\n")


def save_error(message):
    errors = read_data(ERROR_FILE)

    errors.append({
        "error": message,
        "date": str(datetime.now())
    })

    save_data(ERROR_FILE, errors)


def load_default_tables():
    tables = read_data(TABLE_FILE)

    if not tables:
        tables = [
            {
                "id": str(i),
                "table_number": i,
                "category": "Family",
                "seats": 10,
                "status": "Available"
            }
            for i in range(1, 11)
        ]

        save_data(TABLE_FILE, tables)

    return tables


class ViewTable:

    def view_table(self):
        tables = load_default_tables()

        print("\n========== TABLE LIST ==========")
        print(f"{'TABLE NUMBER':<15}{'CATEGORY':<12}{'SEATS':<10}{'STATUS'}")
        print("-" * 55)

        for table in tables:
            print(
                f"{table.get('table_number', 'N/A'):<15}"
                f"{table.get('category', 'N/A'):<12}"
                f"{table.get('seats', 'N/A'):<10}"
                f"{table.get('status', 'N/A')}"
            )

        print("-" * 55)


class BookTable:

    def book_table(self, staff_name=""):
        tables = load_default_tables()
        bookings = read_data(BOOKING_FILE)

        if not staff_name:
            staff_name = input("Enter Staff Name: ")

        if not staff_name.strip():
            print("Staff Name is required.")
            return

        print("\n========== BOOK TABLE ==========")
        print("Staff Name:", staff_name)

        print("\n========== AVAILABLE TABLES ==========")
        print(f"{'TABLE NUMBER':<15}{'CATEGORY':<12}{'SEATS':<10}{'STATUS'}")
        print("-" * 55)

        for table in tables:
            print(
                f"{table.get('table_number', 'N/A'):<15}"
                f"{table.get('category', 'N/A'):<12}"
                f"{table.get('seats', 'N/A'):<10}"
                f"{table.get('status', 'N/A')}"
            )

        table_number = input("\nEnter Table Number (1-10): ").strip()

        if not table_number.isdigit() or not 1 <= int(table_number) <= 10:
            print("Table Number must be between 1 and 10.")
            save_error("Invalid Table Number")
            return

        selected_table = None

        for table in tables:
            if str(table.get("table_number")) == table_number:
                selected_table = table
                break

        if selected_table is None:
            print("Table not found.")
            return

        print(
            f"\nTable Number {table_number} has "
            f"{selected_table.get('seats', 0)} seats."
        )

        if selected_table.get("status") != "Available":
            print("This table is already booked.")
            return

        customer_name = input("Enter Customer Name: ")

        if not customer_name.replace(" ", "").isalpha():
            print("Enter a valid customer name.")
            return

        phone = input("Enter Phone Number: ")

        if len(phone) != 10 or not phone.isdigit():
            print("Phone number must be 10 digits.")
            return

        try:
            people = int(input("Enter Number of People: "))

            if people < 1 or people > 10:
                print("Number of People must be between 1 and 10.")
                return

            if people > int(selected_table.get("seats", 0)):
                print("This table does not have enough seats.")
                return

        except ValueError:
            print("Enter a valid number.")
            save_error("Invalid people count")
            return

        booking_id = str(8000000000 + len(bookings) + 1)
        now = datetime.now()

        booking = {
            "booking_id": booking_id,
            "staff_name": staff_name,
            "table_id": str(selected_table.get("id", "")),
            "table_number": int(table_number),
            "seats": selected_table.get("seats", 10),
            "customer_name": customer_name,
            "phone": phone,
            "people": people,
            "date": str(now.date()),
            "time": str(now.time())[:8],
            "status": "Active"
        }

        bookings.append(booking)
        selected_table["status"] = "Booked"

        save_data(BOOKING_FILE, bookings)
        save_data(TABLE_FILE, tables)

        write_log(f"Table booked successfully: {booking_id}")

        print("\nTable Booked Successfully!")
        print("Booking ID:", booking_id)
        print("Staff Name:", staff_name)
        print("Table Number:", table_number)
        print("Seats:", selected_table.get("seats", "N/A"))


class BookingStatus:

    def booking_status(self):
        bookings = read_data(BOOKING_FILE)

        print("\n========== BOOKING STATUS ==========")

        if not bookings:
            print("No bookings found.")
            return

        for booking in bookings:
            print("-" * 45)

            print("Booking ID:", booking.get("booking_id", booking.get("id", "Not Available")))
            print("Staff Name:", booking.get("staff_name", booking.get("staff_id", "Not Available")))
            print("Table Number:", booking.get("table_number", booking.get("table_id", "Not Available")))
            print("Seats:", booking.get("seats", "Not Available"))
            print("Customer Name:", booking.get("customer_name", "Not Available"))
            print("Phone:", booking.get("phone", booking.get("customer_phone", "Not Available")))
            print("People:", booking.get("people", "Not Available"))
            print("Date:", booking.get("date", "Not Available"))
            print("Time:", booking.get("time", "Not Available"))
            print("Status:", booking.get("status", "Not Available"))

        print("-" * 45)


class CancelBooking:

    def cancel_booking(self):
        bookings = read_data(BOOKING_FILE)
        tables = load_default_tables()

        booking_id = input("Enter Booking ID: ").strip()

        selected_booking = None

        for booking in bookings:
            if booking.get("booking_id") == booking_id:
                selected_booking = booking
                break

        if selected_booking is None:
            print("Booking not found.")
            return

        if selected_booking.get("status") != "Active":
            print("This booking is already cancelled or completed.")
            return

        selected_booking["status"] = "Cancelled"

        for table in tables:
            if str(table.get("id")) == str(selected_booking.get("table_id")):
                table["status"] = "Available"
                break

        save_data(BOOKING_FILE, bookings)
        save_data(TABLE_FILE, tables)

        write_log(f"Booking cancelled: {booking_id}")

        print("Booking Cancelled Successfully!")


class TableMenu:

    def start(self):
        view = ViewTable()
        book = BookTable()
        cancel = CancelBooking()
        status = BookingStatus()

        while True:
            print("\n========== TABLE MANAGEMENT ==========")
            print("1. View Tables")
            print("2. Book Table")
            print("3. Booking Status")
            print("4. Cancel Booking")
            print("5. Back to Main Menu")

            choice = input("Enter Your Choice: ")

            if choice == "1":
                view.view_table()

            elif choice == "2":
                book.book_table()

            elif choice == "3":
                status.booking_status()

            elif choice == "4":
                cancel.cancel_booking()

            elif choice == "5":
                break

            else:
                print("Invalid Choice. Try Again.")
