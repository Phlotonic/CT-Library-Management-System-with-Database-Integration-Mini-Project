# library_system.py
from datetime import datetime, timedelta
import mysql.connector
import book_operations
import user_operations
import author_operations
import reservations_and_fines

class LibraryManagementSystem:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='your_user_name',
            password='your_password',
            database='library_db'
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def main_menu(self):
        while True:
            print("\nWelcome to the Library Management System with Database Integration!")
            print("****")
            print("Main Menu:")
            print("1. Book Operations")
            print("2. User Operations")
            print("3. Author Operations")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.book_operations_menu()
            elif choice == '2':
                self.user_operations_menu()
            elif choice == '3':
                self.author_operations_menu()
            elif choice == '4':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def book_operations_menu(self):
        while True:
            print("\nBook Operations:")
            print("1. Add a new book")
            print("2. Borrow a book")
            print("3. Return a book")
            print("4. Search for a book")
            print("5. Display all books")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                book_operations.add_book(self.cursor, self.conn) 
            elif choice == '2':
                book_operations.borrow_book(self.cursor, self.conn, self)
            elif choice == '3':
                book_operations.return_book(self.cursor, self.conn, self)
            elif choice == '4':
                book_operations.search_book(self.cursor)
            elif choice == '5':
                book_operations.display_books(self.cursor)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")

    def user_operations_menu(self):
        while True:
            print("\nUser Operations:")
            print("1. Add a new user")
            print("2. View user details")
            print("3. Display all users")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                user_operations.add_user(self.cursor, self.conn)
            elif choice == '2':
                user_operations.view_user_details(self.cursor, self)
            elif choice == '3':
                user_operations.display_all_users(self.cursor, self)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def author_operations_menu(self):
        while True:
            print("\nAuthor Operations:")
            print("1. Add a new author")
            print("2. View author details")
            print("3. Display all authors")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                author_operations.add_author(self.cursor, self.conn)
            elif choice == '2':
                author_operations.view_author_details(self.cursor)
            elif choice == '3':
                author_operations.display_all_authors(self.cursor)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    # Additional methods for reservations and fines 
    def reserve_book(self):
        reservations_and_fines.reserve_book(self.cursor, self.conn)

    def check_reservations_for_book(self, book_id):
        """
        Checks for pending reservations for the specified book and notifies the next user in line.
        """
        reservations_and_fines.check_reservations_for_book(self.cursor, self.conn, book_id)

    def calculate_fine(self, user_library_id):
        return reservations_and_fines.calculate_fine(self.cursor, user_library_id)

    def pay_fine(self):
        reservations_and_fines.pay_fine(self.cursor, self.conn, self.calculate_fine)