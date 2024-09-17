import re
from datetime import datetime

class Book:
    def __init__(self, title, author, genre, publication_date, isbn):
        self.__title = title
        self.__author = author
        self.__genre = genre
        self.__publication_date = publication_date
        self.__isbn = isbn
        self.__is_available = True

    # Getters and setters for encapsulation
    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_genre(self):
        return self.__genre

    def get_publication_date(self):
        return self.__publication_date

    def get_isbn(self):
        return self.__isbn

    def is_available(self):
        return self.__is_available

    def borrow(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False

    def return_book(self):
        self.__is_available = True

    @staticmethod
    def validate_isbn(isbn):
        if not re.match(r"^\d{10}$", isbn):
            raise ValueError("Invalid ISBN format. Should be 10 digits.")
        return isbn

    @staticmethod
    def validate_publication_date(publication_date):
        try:
            datetime.strptime(publication_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid publication date format. Should be YYYY-MM-DD.")
        return publication_date