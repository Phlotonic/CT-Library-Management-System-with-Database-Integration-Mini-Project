Library Management System with MySQL Integration

This Python-based library management system provides a command-line interface to perform various operations related to books, users, and authors. It seamlessly integrates with a MySQL database named library_db to ensure data persistence and consistency.

Features

Book Operations:

Add new books to the library
Borrow books (with due date tracking)
Return borrowed books
Search for books by title
Display all books in the library

User Operations:

Add new users to the system
View user details (including borrowed books and fines)
Display all users in the system

Author Operations:

Add new authors to the system
View author details (including books written)
Display all authors in the system

Reservations and Fines:

Reserve unavailable books
Check for available reservations and notify users
Calculate fines for overdue books
Process fine payments
Database Integration

The system utilizes a MySQL database named library_db to store and manage data.

The following tables are used:

books: Stores information about books (title, author, ISBN, publication date, availability).

authors: Stores information about authors (name, biography).

users: Stores information about users (name, library ID).

borrowed_books: Tracks which books are borrowed by which users (user ID, book ID, borrow date, return date).

reservations: Stores information about book reservations (user ID, book ID, reservation date).

fines: (Optional) Tracks fines incurred by users (user ID, borrowed book ID, fine amount, payment status, payment date).

genres: Stores information about book genres (name).

book_genres: Establishes a many-to-many relationship between books and genres.

File Structure

main.py: The main script that initializes the LibraryManagementSystem and starts the main menu loop.

library_system.py: Contains the LibraryManagementSystem class, handling the core logic and interactions with the database.

book_operations.py: Contains functions related to book operations.

user_operations.py: Contains functions related to user operations.

author_operations.py: Contains functions related to author operations.

reservations_and_fines.py: Contains functions for handling reservations and fines.

How to Use

Set up the database:

Create a MySQL database named library_db, or use the included one with a similar name.
Execute the SQL queries provided to create the necessary tables.

Install dependencies:

Make sure you have the mysql.connector library installed. You can install it using pip:

Bash
pip install mysql-connector-python

Run the system:

Execute the main.py script from your terminal or IDE.
Follow the on-screen prompts to navigate the menus and perform various library operations.

Additional Notes

The system includes basic error handling and input validation, but you might want to enhance it further for a more robust user experience.
Consider adding more features and functionalities based on your specific requirements.
Ensure that your MySQL server is running and accessible, and that the database connection details in library_system.py are correct.
Feel free to contribute, report issues, or suggest improvements!

Contact
For any questions or suggestions, please contact me at adryden508@gmail.com.
