from datetime import datetime

def reserve_book(cursor, conn):
    title = input("Enter the title of the book to reserve: ")
    user_library_id = input("Enter your library ID: ")

    try:
        # Check if the book exists
        cursor.execute("SELECT id, availability FROM books WHERE title = %s", (title,))
        book_result = cursor.fetchone()

        if not book_result:
            print("Book not found.")
            return

        book_id, availability = book_result

        if availability:
            print("Book is currently available. You can borrow it instead.")
            return

        # Check if the user exists
        cursor.execute("SELECT id FROM users WHERE library_id = %s", (user_library_id,))
        user_id_result = cursor.fetchone()
        if not user_id_result:
            print("User not found.")
            return

        user_id = user_id_result[0]

        # Check if the user already has a reservation for this book
        cursor.execute(
            "SELECT id FROM reservations WHERE user_id = %s AND book_id = %s",
            (user_id, book_id)
        )
        existing_reservation = cursor.fetchone()
        if existing_reservation:
            print("You already have a reservation for this book.")
            return

        # Create a reservation
        reservation_date = datetime.now().date()
        cursor.execute(
            "INSERT INTO reservations (user_id, book_id, reservation_date) VALUES (%s, %s, %s)",
            (user_id, book_id, reservation_date)
        )
        conn.commit()
        print("Book reserved successfully!")
    except mysql.connector.Error as err:
        print(f"Error reserving book: {err}")
        conn.rollback()

def check_reservations_for_book(cursor, conn, book_id):
    """
    Checks for pending reservations for the specified book and notifies the next user in line.
    """
    try:
        # Fetch the oldest reservation for the book
        cursor.execute(
            "SELECT r.id, r.user_id, b.title "
            "FROM reservations r "
            "JOIN books b ON r.book_id = b.id "
            "WHERE r.book_id = %s "
            "ORDER BY r.reservation_date ASC "
            "LIMIT 1",
            (book_id,)
        )
        reservation = cursor.fetchone()

        if reservation:
            reservation_id, user_id, book_title = reservation

            # Fetch user's name
            cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            user_name = cursor.fetchone()[0]

            print(f"Notification: Book '{book_title}' is now available for user {user_name}.")

            # Delete the reservation
            cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
            conn.commit()
    except mysql.connector.Error as err:
        print(f"Error checking reservations: {err}")
        conn.rollback()

def calculate_fine(cursor, user_library_id):
    # Fetch all overdue books for the user
    cursor.execute(
        "SELECT bb.borrow_date "
        "FROM borrowed_books bb "
        "JOIN users u ON bb.user_id = u.id "
        "WHERE u.library_id = %s AND bb.return_date IS NULL AND DATE_ADD(bb.borrow_date, INTERVAL 14 DAY) < CURDATE()",
        (user_library_id,)
    )
    overdue_books = cursor.fetchall()

    total_fine = 0
    for borrow_date, in overdue_books:
        days_overdue = (datetime.now().date() - borrow_date).days
        fine = days_overdue * 1  # $1 fine per day
        total_fine += fine

    return total_fine

def pay_fine(cursor, conn, calculate_fine_func):
    user_library_id = input("Enter your library ID: ")
    fine = calculate_fine_func(cursor, user_library_id)

    if fine > 0:
        print(f"Total fine: ${fine}")
        while True:
            try:
                payment = float(input("Enter payment amount: "))
                if payment >= fine:
                    try:
                        cursor.execute(
                            "INSERT INTO fines (user_id, fine_amount, payment_status, payment_date) "
                            "VALUES ((SELECT id FROM users WHERE library_id = %s), %s, 'paid', CURDATE())",
                            (user_library_id, fine)
                        )
                        conn.commit()
                        print("Fine paid successfully!")
                        break
                    except mysql.connector.Error as err:
                        print(f"Error recording fine payment: {err}")
                        conn.rollback() 
                else:
                    print("Insufficient payment. Please pay the full amount.")
            except ValueError:
                print("Invalid payment amount. Please enter a number.")
    else:
        print("No fines to pay.")