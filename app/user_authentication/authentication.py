
import json
import os
import maskpass
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_FILE = os.path.join(BASE_DIR, "database", "users.json")
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


def password_input(prompt):
    return maskpass.askpass(prompt)


class UserAuthentication:

    def login(self):
        users = read_data(USER_FILE)

        print("\n===== ADMIN SIGN IN =====")

        username = input("Enter Username: ")

        if username == "":
            print("Username cannot be empty!")
            save_error("Empty username")
            return None

        if not username.isalnum():
            print("Invalid Username!")
            save_error("Invalid username")
            return None

        password = password_input("Enter Password: ")

        if password == "":
            print("Password cannot be empty!")
            save_error("Empty password")
            return None

        if len(password) < 6:
            print("Password must be at least 6 characters!")
            save_error("Short password")
            return None

        for user in users:
            if (
                user.get("username") == username
                and user.get("password") == password
                and user.get("role") == "Admin"
                and user.get("status") == "Active"
            ):
                print("\nAdmin Login Successful!")
                print("Welcome Admin!")
                write_log("Admin login successful")
                return user

        print("\nInvalid Username or Password!")
        save_error("Admin login failed")
        return None

    def staff_login(self):
        users = read_data(USER_FILE)

        print("\n===== STAFF SIGN IN =====")

        username = input("Enter Staff Username: ")

        if username == "":
            print("Username cannot be empty!")
            return None

        password = password_input("Enter Password: ")

        if password == "":
            print("Password cannot be empty!")
            return None

        for user in users:
            if (
                user.get("username") == username
                and user.get("password") == password
                and user.get("role") == "Staff"
                and user.get("status") == "Active"
            ):
                print("\nStaff Login Successful!")
                print("Welcome", user.get("username"), "!")
                write_log("Staff login successful: " + user.get("username"))
                return user

        print("\nInvalid Staff Username or Password!")
        save_error("Staff login failed")
        return None


class UserMenu:

    def start(self):
        auth = UserAuthentication()

        while True:
            print("\n===== THE ROYAL PLATE =====")
            print("1. Admin Sign In")
            print("2. Staff Sign In")
            print("3. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                user = auth.login()

                if user:
                    return user

            elif choice == "2":
                user = auth.staff_login()

                if user:
                    return user

            elif choice == "3":
                print("Thank You!")
                return None

            else:
                print("Invalid Choice!")


class StaffManagement:

    def generate_staff_id(self, users):
        numbers = []

        for user in users:
            staff_id = user.get("staff_id", "")

            if staff_id.startswith("ST"):
                try:
                    numbers.append(int(staff_id[2:]))
                except ValueError:
                    pass

        next_number = max(numbers, default=100) + 1

        return "ST" + str(next_number)

    def add_staff(self):
        users = read_data(USER_FILE)

        print("\n===== ADD STAFF =====")

        username = input("Enter Staff Username: ")

        if username == "":
            print("Username cannot be empty!")
            return

        if not username.isalnum():
            print("Username must contain letters and numbers only!")
            return

        for user in users:
            if user.get("username") == username:
                print("Username Already Exists!")
                return

        password = password_input("Enter Password: ")

        if password == "":
            print("Password cannot be empty!")
            return

        if len(password) < 6:
            print("Password must be at least 6 characters!")
            return

        staff_id = self.generate_staff_id(users)

        staff = {
            "staff_id": staff_id,
            "username": username,
            "password": password,
            "role": "Staff",
            "status": "Active",
            "date": str(datetime.now().date()),
            "time": str(datetime.now().time())
        }

        users.append(staff)
        save_data(USER_FILE, users)

        write_log("New staff added")

        print("Staff Added Successfully!")
        print("Staff ID:", staff_id)

    def view_staff(self):
        users = read_data(USER_FILE)

        print("\n===== STAFF INFORMATION =====")

        found = False

        for user in users:
            if user.get("role") == "Staff":
                found = True

                print("\nStaff ID:", user.get("staff_id", "Not Assigned"))
                print("Username:", user.get("username"))
                print("Role:", user.get("role"))
                print("Status:", user.get("status"))
                print("Date:", user.get("date"))

        if not found:
            print("No Staff Found!")

    def update_staff(self):
        users = read_data(USER_FILE)

        print("\n===== UPDATE STAFF =====")

        username = input("Enter Staff Username: ")

        for user in users:
            if (
                user.get("username") == username
                and user.get("role") == "Staff"
            ):
                while True:
                    print("\n1. Change Username")
                    print("2. Change Password")
                    print("3. Change Status")
                    print("4. Back")

                    choice = input("Enter Choice: ")

                    if choice == "1":
                        new_username = input("Enter New Username: ")

                        if new_username == "" or not new_username.isalnum():
                            print("Invalid Username!")
                            continue

                        exists = False

                        for other in users:
                            if other.get("username") == new_username:
                                exists = True

                        if exists:
                            print("Username Already Exists!")
                            continue

                        user["username"] = new_username
                        save_data(USER_FILE, users)
                        write_log("Staff username changed")

                        print("Username Updated Successfully!")
                        return

                    elif choice == "2":
                        new_password = password_input("Enter New Password: ")

                        if new_password == "":
                            print("Password cannot be empty!")
                            continue

                        if len(new_password) < 6:
                            print("Password must be at least 6 characters!")
                            continue

                        user["password"] = new_password
                        save_data(USER_FILE, users)
                        write_log("Staff password changed")

                        print("Password Updated Successfully!")
                        return

                    elif choice == "3":
                        print("1. Active")
                        print("2. Inactive")

                        status_choice = input("Enter Choice: ")

                        if status_choice == "1":
                            user["status"] = "Active"
                        elif status_choice == "2":
                            user["status"] = "Inactive"
                        else:
                            print("Invalid Choice!")
                            continue

                        save_data(USER_FILE, users)
                        write_log("Staff status updated")

                        print("Staff Status Updated Successfully!")
                        return

                    elif choice == "4":
                        return

                    else:
                        print("Invalid Choice!")

        print("Staff Not Found!")

    def delete_staff(self):
        users = read_data(USER_FILE)

        username = input("Enter Staff Username: ")

        new_users = []
        found = False

        for user in users:
            if (
                user.get("username") == username
                and user.get("role") == "Staff"
            ):
                found = True
            else:
                new_users.append(user)

        if found:
            save_data(USER_FILE, new_users)
            write_log("Staff deleted")
            print("Staff Deleted Successfully!")
        else:
            print("Staff Not Found!")

    def start(self):
        while True:
            print("\n===== STAFF MANAGEMENT =====")
            print("1. Add Staff")
            print("2. View Staff")
            print("3. Update Staff")
            print("4. Delete Staff")
            print("5. Back")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.add_staff()
            elif choice == "2":
                self.view_staff()
            elif choice == "3":
                self.update_staff()
            elif choice == "4":
                self.delete_staff()
            elif choice == "5":
                break
            else:
                print("Invalid Choice!")


if __name__ == "__main__":
    UserMenu().start()
