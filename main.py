from book import Book
from user import User
from author import Author
from reservation import Reservation
from borrowed_book import BorrowedBook
from datetime import datetime, timedelta

def main_menu():
    print("Welcome to the Library Management System!")
    print("Main Menu:")
    print("1. Book Operations")
    print("2. User Operations")
    print("3. Author Operations")
    print("4. Quit")

    choice = input("Enter your choice: ")
    return choice

def book_operations_menu():
    print("Book Operations:")
    print("1. Add a new book")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Search for a book")
    print("5. Display all books")

    choice = input("Enter your choice: ")
    return choice

def user_operations_menu():
    print("User Operations:")
    print("1. Add a new user")
    print("2. View user details")
    print("3. Display all users")

    choice = input("Enter your choice: ")
    return choice

def author_operations_menu():
    print("Author Operations:")
    print("1. Add a new author")
    print("2. View author details")
    print("3. Display all authors")

    choice = input("Enter your choice: ")
    return choice

def add_new_book(library):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    genre = input("Enter book genre: ")
    publication_date = input("Enter publication date (YYYY-MM-DD): ")
    isbn = input("Enter ISBN (10 digits): ")

    try:
        publication_date = Book.validate_publication_date(publication_date)
        isbn = Book.validate_isbn(isbn)
    except ValueError as e:
        print(e)
        return

    new_book = Book(title, author, genre, publication_date, isbn)
    library.append(new_book)
    print("Book added successfully!")

def borrow_book_with_due_date(library, user):
    title = input("Enter the title of the book to borrow: ")
    for book in library:
        if book.get_title() == title:
            if book.borrow():
                due_date = datetime.now() + timedelta(days=14)  # 2 weeks due date
                new_book = BorrowedBook(title, due_date)
                user.borrow_book(new_book)
                print(f"Book borrowed successfully! Due date: {due_date.strftime('%Y-%m-%d')}")
            else:
                print("Book is currently unavailable.")
            return
    print("Book not found.")

def return_book(library, user):
    title = input("Enter the title of the book to return: ")
    for book in library:
        if book.get_title() == title:
            book.return_book()
            user.return_book(title)
            print("Book returned successfully!")
            return
    print("Book not found.")

def search_book(library):
    title = input("Enter the title of the book to search: ")
    for book in library:
        if book.get_title() == title:
            print(f"Title: {book.get_title()}")
            print(f"Author: {book.get_author()}")
            print(f"Genre: {book.get_genre()}")
            print(f"Publication Date: {book.get_publication_date()}")
            print(f"ISBN: {book.get_isbn()}")
            print(f"Availability: {'Available' if book.is_available() else 'Borrowed'}")
            return
    print("Book not found.")

def display_all_books(library):
    for book in library:
        print(f"Title: {book.get_title()}, Author: {book.get_author()}, Genre: {book.get_genre()}, Publication Date: {book.get_publication_date()}, ISBN: {book.get_isbn()}, Availability: {'Available' if book.is_available() else 'Borrowed'}")

def add_new_user(users):
    name = input("Enter user name: ")
    library_id = input("Enter library ID (5 digits): ")

    try:
        library_id = User.validate_library_id(library_id)
    except ValueError as e:
        print(e)
        return

    new_user = User(name, library_id)
    users.append(new_user)
    print("User added successfully!")

def view_user_details(users):
    library_id = input("Enter library ID: ")
    for user in users:
        if user.get_library_id() == library_id:
            print(f"Name: {user.get_name()}")
            print(f"Library ID: {user.get_library_id()}")
            print(f"Borrowed Books: {', '.join(user.get_borrowed_books())}")
            return
    print("User not found.")

def display_all_users(users):
    for user in users:
        print(f"Name: {user.get_name()}, Library ID: {user.get_library_id()}, Borrowed Books: {', '.join(user.get_borrowed_books())}")

def add_new_author(authors):
    name = input("Enter author name: ")
    biography = input("Enter author biography: ")

    new_author = Author(name, biography)
    authors.append(new_author)
    print("Author added successfully!")

def view_author_details(authors):
    name = input("Enter author name: ")
    for author in authors:
        if author.get_name() == name:
            print(f"Name: {author.get_name()}")
            print(f"Biography: {author.get_biography()}")
            return
    print("Author not found.")

def display_all_authors(authors):
    for author in authors:
        print(f"Name: {author.get_name()}, Biography: {author.get_biography()}")

def reserve_book(library, reservations, user):
    title = input("Enter the title of the book to reserve: ")
    for book in library:
        if book.get_title() == title:
            if not book.is_available():
                new_reservation = Reservation(title, user.get_library_id())
                reservations.append(new_reservation)
                print("Book reserved successfully!")
            else:
                print("Book is available. You can borrow it instead.")
            return
    print("Book not found.")

def check_reservations(library, reservations, users):
    for reservation in reservations:
        for book in library:
            if book.get_title() == reservation.get_book_title() and book.is_available():
                for user in users:
                    if user.get_library_id() == reservation.get_user_id():
                        print(f"Notification: Book '{book.get_title()}' is now available for user {user.get_name()}.")
                        reservations.remove(reservation)
                        break

def calculate_fine(user):
    total_fine = 0
    for borrowed_book in user.get_borrowed_books():
        due_date = borrowed_book.get_due_date()
        if datetime.now() > due_date:
            days_overdue = (datetime.now() - due_date).days
            fine = days_overdue * 1  # $1 fine per day
            total_fine += fine
    return total_fine

def pay_fine(user):
    fine = calculate_fine(user)
    if fine > 0:
        print(f"Total fine: ${fine}")
        payment = input("Enter payment amount: ")
        if float(payment) >= fine:
            user.clear_fines()
            print("Fine paid successfully!")
        else:
            print("Insufficient payment. Please pay the full amount.")
    else:
        print("No fines to pay.")

def main():
    library = []
    users = []
    authors = []
    reservations = []

    while True:
        choice = main_menu()
        if choice == '1':
            book_choice = book_operations_menu()
            if book_choice == '1':
                add_new_book(library)
            elif book_choice == '2':
                user_id = input("Enter your library ID: ")
                for user in users:
                    if user.get_library_id() == user_id:
                        borrow_book_with_due_date(library, user)
                        break
                else:
                    print("User not found.")
            elif book_choice == '3':
                user_id = input("Enter your library ID: ")
                for user in users:
                    if user.get_library_id() == user_id:
                        return_book(library, user)
                        break
                else:
                    print("User not found.")
            elif book_choice == '4':
                search_book(library)
            elif book_choice == '5':
                display_all_books(library)
        elif choice == '2':
            user_choice = user_operations_menu()
            if user_choice == '1':
                add_new_user(users)
            elif user_choice == '2':
                view_user_details(users)
            elif user_choice == '3':
                display_all_users(users)
        elif choice == '3':
            author_choice = author_operations_menu()
            if author_choice == '1':
                add_new_author(authors)
            elif author_choice == '2':
                view_author_details(authors)
            elif author_choice == '3':
                display_all_authors(authors)
        elif choice == '4':
            print("Quitting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        # Check reservations and notify users
        check_reservations(library, reservations, users)

if __name__ == "__main__":
    main()