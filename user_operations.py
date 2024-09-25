# user_operations.py

import mysql.connector

# user_operations.py
def add_user(cursor, conn):
    name = input("Enter user name: ")
    library_id = input("Enter library ID (10 characters max): ")

    try:
        # Check if library_id already exists
        cursor.execute("SELECT * FROM users WHERE library_id = %s", (library_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            print("Library ID already exists. Please choose a different one.")
            return

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (name, library_id) VALUES (%s, %s)", (name, library_id))
        conn.commit()  # Commit the changes using the conn object
        print("User added successfully!")
    except mysql.connector.Error as err:
        print(f"Error adding user: {err}")
        conn.rollback()

def view_user_details(cursor, lms):  # Add 'lms' as an argument
    library_id = input("Enter library ID: ")

    try:
        # Fetch user details from the database
        cursor.execute("SELECT name, library_id FROM users WHERE library_id = %s", (library_id,))
        result = cursor.fetchone()

        if result:
            name, library_id = result
            print(f"Name: {name}")
            print(f"Library ID: {library_id}")

            # Fetch borrowed books for this user
            cursor.execute(
                "SELECT b.title "
                "FROM borrowed_books bb "
                "JOIN books b ON bb.book_id = b.id "
                "WHERE bb.user_id = (SELECT id FROM users WHERE library_id = %s) AND bb.return_date IS NULL",
                (library_id,)
            )
            borrowed_books = [row[0] for row in cursor.fetchall()]
            print(f"Borrowed Books: {', '.join(borrowed_books) if borrowed_books else 'None'}")

            # Calculate and display any outstanding fines
            fine = lms.calculate_fine(library_id)  # Call calculate_fine on the lms object

            if fine > 0:
                print(f"Outstanding Fine: ${fine}")
            else:
                print("No outstanding fines.")
        else:
            print("User not found.")
    except mysql.connector.Error as err:
        print(f"Error viewing user details: {err}")

def display_all_users(cursor, lms):  # Pass the lms object as an argument
    try:
        # Fetch all users from the database
        cursor.execute("SELECT id, name, library_id FROM users")
        user_data = cursor.fetchall()

        for user_id, name, library_id in user_data:
            # Fetch borrowed books for this user
            cursor.execute(
                "SELECT b.title "
                "FROM borrowed_books bb "
                "JOIN books b ON bb.book_id = b.id "
                "WHERE bb.user_id = %s AND bb.return_date IS NULL",
                (user_id,)
            )
            borrowed_books = [row[0] for row in cursor.fetchall()]

            # Calculate and display any outstanding fines
            fine = lms.calculate_fine(library_id)  # Call calculate_fine on the lms object

            print(
                f"Name: {name}, Library ID: {library_id}, "
                f"Borrowed Books: {', '.join(borrowed_books) if borrowed_books else 'None'}"
                f", Outstanding Fine: ${fine if fine > 0 else 'None'}"
            )
    except mysql.connector.Error as err:
        print(f"Error displaying users: {err}")