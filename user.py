import re
from datetime import datetime

class User:
    def __init__(self, name, library_id):
        self.__name = name
        self.__library_id = library_id
        self.__borrowed_books = []

    def get_name(self):
        return self.__name

    def get_library_id(self):
        return self.__library_id

    def get_borrowed_books(self):
        return [book.get_book_title() for book in self.__borrowed_books]

    def borrow_book(self, borrowed_book):
        self.__borrowed_books.append(borrowed_book)

    def return_book(self, book_title):
        for borrowed_book in self.__borrowed_books:
            if borrowed_book.get_book_title() == book_title:
                self.__borrowed_books.remove(borrowed_book)
                return
        print("Book not found in borrowed books.")

    def clear_fines(self):
        # Add a method to clear fines
        self.__borrowed_books = [book for book in self.__borrowed_books if datetime.now() <= book.get_due_date()]

    @staticmethod
    def calculate_fine(user):
        total_fine = 0
        for borrowed_book in user.__borrowed_books:
            due_date = borrowed_book.get_due_date()
            if datetime.now() > due_date:
                days_overdue = (datetime.now() - due_date).days
                fine = days_overdue * 1  # $1 fine per day
                total_fine += fine
        return total_fine

    @staticmethod
    def validate_library_id(library_id):
        if not re.match(r"^\d{5}$", library_id):
            raise ValueError("Invalid library ID format. Should be 5 digits.")
        return library_id