class Reservation:
    def __init__(self, book_title, user_id):
        self.__book_title = book_title
        self.__user_id = user_id

    # Getters for encapsulation
    def get_book_title(self):
        return self.__book_title

    def get_user_id(self):
        return self.__user_id