from datetime import datetime

class BorrowedBook:
    def __init__(self, book_title, due_date):
        self.__book_title = book_title
        self.__due_date = due_date

    def get_book_title(self):
        return self.__book_title

    def get_due_date(self):
        return self.__due_date