# book_operations.py
from datetime import datetime
import mysql.connector 

def add_book(cursor, conn):
        title = input("Enter book title: ")
        author_name = input("Enter book author name: ")
        isbn = input("Enter ISBN (13 digits): ")
        publication_date_str = input("Enter publication date (YYYY-MM-DD): ")
        genres = input("Enter genres (comma-separated): ").split(",")

        try:
            publication_date = datetime.strptime(publication_date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            # Get or create author
            cursor.execute("SELECT id FROM authors WHERE name = %s", (author_name,))
            author_id_result = cursor.fetchone()
            if author_id_result:
                author_id = author_id_result[0]
            else:
                cursor.execute("INSERT INTO authors (name) VALUES (%s)", (author_name,))
                author_id = cursor.lastrowid

            # Insert the new book
            cursor.execute(
                "INSERT INTO books (title, author_id, isbn, publication_date) VALUES (%s, %s, %s, %s)",
                (title, author_id, isbn, publication_date)
            )
            book_id = cursor.lastrowid

            # Insert book genres
            for genre in genres:
                genre = genre.strip()  # Remove leading/trailing spaces
                cursor.execute("SELECT id FROM genres WHERE name = %s", (genre,))
                genre_id_result = cursor.fetchone()
                if genre_id_result:
                    genre_id = genre_id_result[0]
                else:
                    cursor.execute("INSERT INTO genres (name) VALUES (%s)", (genre,))
                    genre_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO book_genres (book_id, genre_id) VALUES (%s, %s)",
                    (book_id, genre_id)
                )

            conn.commit()
            print("Book added successfully!")
        except mysql.connector.Error as err:
            print(f"Error adding book: {err}")
            conn.rollback()

def borrow_book(cursor, conn, lms):
    title = input("Enter the title of the book to borrow: ")
    user_library_id = input("Enter your library ID: ")

    try:
        # Check if the book exists and is available
        cursor.execute("SELECT id FROM books WHERE title = %s AND availability = 1", (title,))
        book_id_result = cursor.fetchone()
        if not book_id_result:
            print("Book not found or currently unavailable.")
            return
    
        # Check if the user exists
        cursor.execute("SELECT id FROM users WHERE library_id = %s", (user_library_id,))
        user_id_result = cursor.fetchone()
        if not user_id_result:
            print("User not found.")
            return
    
        book_id = book_id_result[0]
        user_id = user_id_result[0]
    
        # Mark the book as unavailable
        cursor.execute("UPDATE books SET availability = 0 WHERE id = %s", (book_id,))
    
        # Create a borrowed_books record
        borrow_date = datetime.now().date()
        cursor.execute(
            "INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, %s)",
            (user_id, book_id, borrow_date)
        )
        conn.commit()
        print("Book borrowed successfully!")

        # Check for any pending reservations for this book and notify the next user in line
        lms.check_reservations_for_book(book_id)
    except mysql.connector.Error as err:
        print(f"Error borrowing book: {err}")
        conn.rollback()

def return_book(cursor, conn, lms):
    title = input("Enter the title of the book to return: ")
    user_library_id = input("Enter your library ID: ")

    try:
        # Check if the book exists and is borrowed
        cursor.execute("SELECT id FROM books WHERE title = %s AND availability = 0", (title,))
        book_id_result = cursor.fetchone()
        if not book_id_result:
            print("Book not found or not currently borrowed.")
            return
    
        # Check if the user exists and has borrowed this book
        cursor.execute(
            "SELECT id FROM users WHERE library_id = %s AND id IN (SELECT user_id FROM borrowed_books WHERE book_id = %s AND return_date IS NULL)",
            (user_library_id, book_id_result[0])
        )
        user_id_result = cursor.fetchone()
        if not user_id_result:
            print("User not found or hasn't borrowed this book.")
            return
    
        book_id = book_id_result[0]
    
        # Mark the book as available
        cursor.execute("UPDATE books SET availability = 1 WHERE id = %s", (book_id,))
    
        # Update the borrowed_books record with return_date
        return_date = datetime.now().date()
        cursor.execute(
            "UPDATE borrowed_books SET return_date = %s WHERE book_id = %s AND return_date IS NULL",
            (return_date, book_id)
        )
        conn.commit()
        print("Book returned successfully!")

        # Check for any pending reservations for this book and notify the next user in line
        lms.check_reservations_for_book(book_id)
    except mysql.connector.Error as err:
        print(f"Error returning book: {err}")
        conn.rollback()

def search_book(cursor):
    title = input("Enter the title of the book to search: ")

    # Search for the book
    cursor.execute(
        "SELECT b.title, a.name, b.isbn, b.publication_date, b.availability "
        "FROM books b "
        "JOIN authors a ON b.author_id = a.id "
        "WHERE b.title = %s",
        (title,)
    )
    result = cursor.fetchone()

    if result:
        title, author_name, isbn, publication_date, availability = result
        print(f"Title: {title}")
        print(f"Author: {author_name}")
        print(f"ISBN: {isbn}")
        print(f"Publication Date: {publication_date}")
        print(f"Availability: {'Available' if availability else 'Borrowed'}")
    else:
        print("Book not found.")

def display_books(cursor):
    # Fetch all books with author names and genres
    cursor.execute(
        "SELECT b.title, a.name, b.isbn, b.publication_date, b.availability, "
        "GROUP_CONCAT(g.name SEPARATOR ', ') AS genres "
        "FROM books b "
        "JOIN authors a ON b.author_id = a.id "
        "LEFT JOIN book_genres bg ON b.id = bg.book_id "
        "LEFT JOIN genres g ON bg.genre_id = g.id "
        "GROUP BY b.id" 
    )
    results = cursor.fetchall()

    for row in results:
        title, author_name, isbn, publication_date, availability, genres = row
        print(
            f"Title: {title}, Author: {author_name}, ISBN: {isbn}, "
            f"Publication Date: {publication_date}, Genres: {genres}, "
            f"Availability: {'Available' if availability else 'Borrowed'}"
        )