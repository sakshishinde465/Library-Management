
README

Introduction

This is a Python and MongoDB-based library management system. It allows users to borrow and reserve books, and librarians to manage books, fines, and users. The system also features a dashboard for librarians to view available and borrowed books, and to manage users and books.

Dependencies

The following Python packages are required to run this system:

APScheduler==3.10.4
blinker==1.6.3
cachelib==0.10.2
click==8.1.7
colorama==0.4.6
DateTime==5.2
dnspython==2.4.2
Flask==3.0.0
Flask-Session==0.5.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
pymongo==4.5.0
pytz==2023.3.post1
setuptools==68.2.2
six==1.16.0
tzdata==2023.3
tzlocal==5.1
Werkzeug==3.0.0
zope.interface==6.1
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