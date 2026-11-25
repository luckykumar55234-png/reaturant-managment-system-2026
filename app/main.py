
from user_authentication.authentication import UserAuthentication, StaffManagement
from menu_menegement.menu import MenuDisplay
from inventory_management.inventory import InventoryMenu
from order_management.order_management import OrderMenu
from table_booking.table_booking import ViewTable, BookTable, CancelBooking, BookingStatus
from billing.billing import BillingMenu


def main():

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
                break

        elif choice == "2":
            user = auth.staff_login()

            if user:
                break

        elif choice == "3":
            print("Thank You!")
            return

        else:
            print("Invalid Choice!")

    if user.get("role") == "Admin":

        staff = StaffManagement()

        table_view = ViewTable()
        table_book = BookTable()
        table_cancel = CancelBooking()
        table_status = BookingStatus()

        while True:

            print("\n========== THE ROYAL PLATE ==========")
            print("             ADMIN MAIN MENU")
            print("-------------------------------------")
            print("1. Staff Management")
            print("2. Menu Management")
            print("3. Order Management")
            print("4. Billing")
            print("5. Inventory Management")
            print("6. View Table")
            print("7. Book Table")
            print("8. Cancel Booking")
            print("9. Booking Status")
            print("10. User Information")
            print("11. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                staff.start()

            elif choice == "2":
                MenuDisplay().start()

            elif choice == "3":
                OrderMenu().start()

            elif choice == "4":
                BillingMenu().start()

            elif choice == "5":
                InventoryMenu().start()

            elif choice == "6":
                table_view.view_table()

            elif choice == "7":
                table_book.book_table(user.get("username", ""))

            elif choice == "8":
                table_cancel.cancel_booking()

            elif choice == "9":
                table_status.booking_status()

            elif choice == "10":
                staff.view_staff()

            elif choice == "11":
                print("Thank You!")
                return

            else:
                print("Invalid Choice!")

    elif user.get("role") == "Staff":

        table_view = ViewTable()
        table_book = BookTable()
        table_status = BookingStatus()

        while True:

            print("\n========== THE ROYAL PLATE ==========")
            print("             STAFF MAIN MENU")
            print("-------------------------------------")
            print("1. Order Management")
            print("2. Billing")
            print("3. View Table")
            print("4. Book Table")
            print("5. Booking Status")
            print("6. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                OrderMenu().start()

            elif choice == "2":
                BillingMenu().start()

            elif choice == "3":
                table_view.view_table()

            elif choice == "4":
                table_book.book_table(user.get("username", ""))

            elif choice == "5":
                table_status.booking_status()

            elif choice == "6":
                print("Thank You!")
                return

            else:
                print("Invalid Choice!")


if __name__ == "__main__":
    main()





    