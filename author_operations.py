def add_author(cursor, conn):
    name = input("Enter author name: ")
    biography = input("Enter author biography: ")

    try:
        # Check if author already exists
        cursor.execute("SELECT * FROM authors WHERE name = %s", (name,))
        existing_author = cursor.fetchone()
        if existing_author:
            print("Author already exists.")
            return

        # Insert the new author into the database
        cursor.execute("INSERT INTO authors (name, biography) VALUES (%s, %s)", (name, biography))
        conn.commit()
        print("Author added successfully!")
    except mysql.connector.Error as err:
        print(f"Error adding author: {err}")
        conn.rollback()

def view_author_details(cursor):
    name = input("Enter author name: ")

    try:
        # Fetch author details from the database
        cursor.execute("SELECT name, biography FROM authors WHERE name = %s", (name,))
        result = cursor.fetchone()

        if result:
            name, biography = result
            print(f"Name: {name}")
            print(f"Biography: {biography}")

            # Fetch books written by this author
            cursor.execute("SELECT title FROM books WHERE author_id = (SELECT id FROM authors WHERE name = %s)", (name,))
            books_written = [row[0] for row in cursor.fetchall()]
            print(f"Books Written: {', '.join(books_written) if books_written else 'None'}")
        else:
            print("Author not found.")
    except mysql.connector.Error as err:
        print(f"Error viewing author details: {err}")

def display_all_authors(cursor):
    try:
        # Fetch all authors from the database
        cursor.execute("SELECT name, biography FROM authors")
        results = cursor.fetchall()

        for name, biography in results:
            print(f"Name: {name}, Biography: {biography}")
    except mysql.connector.Error as err:
        print(f"Error displaying authors: {err}")