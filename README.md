README

Introduction

This is a Python and MongoDB-based library management system. It allows users to borrow and reserve books, and librarians to manage books, fines, and users. The system also features a dashboard for librarians to view available and borrowed books, and to manage users and books.

Installation

To install the required dependencies, run the following command in your terminal:

pip install -r requirements.txt
Once the dependencies are installed, you can start the system by running the following command:

python main.py
Features

User authentication: Users can log in to the system to access their account and manage their books.
Book management: Librarians can add, delete, and update books in the system.
Fine management: Fines are calculated automatically for overdue books. Late fees of Rs.5 per day are applied.
Librarian dashboard: Librarians can view available and borrowed books, and manage users and books from the dashboard.
Security: Password hashes are generated so that passwords are not visible even in the database. Login authentication is performed.
Logging and error handling: Logging and error handling is performed, and logs are maintained.
User profiles: Users can create and manage their profiles.
Borrowing system: Users can borrow books and reserve them. Automatic due dates are generated, and a period of 14 days is given.
Reservation system: Users can reserve books that are currently checked out.
Usage

To use the system, users can log in to their account and browse the available books. To borrow a book, users can click on the "Borrow" button next to the book. To reserve a book, users can click on the "Reserve" button next to the book.

Librarians can access the dashboard by logging in to their account and clicking on the "Dashboard" link in the navigation bar. From the dashboard, librarians can view available and borrowed books, and manage users and books.

Conclusion

This is a comprehensive library management system that is easy to use and manage. It is a great solution for libraries of all sizes.
