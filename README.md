# library-database-system

## Description
A library management desktop application made using Python, Tkinter (GUI) and MySQL. It's designed to help manage library operations such as tracking books, managing checkouts, check-ins, and handling fines.

## Features

- **Book Search:** Users can search for books by title, author, or ISBN.
- **Check Out/In:** Facilitates the check-out and check-in processes.
- **Fine Management:** Automatically calculates and manages fines.
- **Borrower Management:** Add and manage borrower information.

## Prerequisites

0. Clone the repository
1. Python
2. Install the libraries mentioned in requirements.txt \
```pip install -r requirements.txt```

## Set-up

0. Change the `db_url` variable in all modules to the corresponding database url (I realize this is not efficient. I'll fix it ...eventually)
1. Run schema.py to create the tables in the database \
```python schema.py```
2. Run the python scripts in `/scripts` to populate the Book, Author, Book_Author and Borrower tables.
3. Run the application using the command \
```python main.py```

## Feedback
For any queries or feedback, please reach out at raaedahmed23@gmail.com