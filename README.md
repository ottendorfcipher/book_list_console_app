## Simple Book Management System
A minimal console application for managing a book collection and exporting it to CSV format.

### Description
This simple Python application allows users to maintain a list of books with basic information:

- Book title
- Author's first and last name
- Price

The program runs in the console/terminal and provides a straightforward way to add, view, and delete books before exporting the collection to a CSV file.

### Features
- Add new books with title, author details, and price
- View the entire book collection in a formatted table
- Delete books by index number
- Export the collection to a CSV file

### Requirements
Python 3.x

### Usage
Clone or download this repository

### Run the script:

``` python book_manager.py ``` 

### Follow the menu prompts:
Enter 1 to add a book
Enter 2 to view your book collection
Enter 3 to delete a book
Enter 4 to export to CSV
Enter 5 to exit the program

### CSV Export
The exported CSV file contains the following columns:

- title
- author_first_name
- author_last_name
- price

You can specify a custom filename during export or use the default books.csv.

### Limitations
- Data is not persistent between program runs (books are stored in memory)
- No search or sorting functionality
- No input validation for text fields
- Limited error handling

### Future Improvements
Potential enhancements for future versions:

- Save/load book data for persistence between sessions
- Add search functionality
- Implement sorting options
- Create a simple GUI

### License
Feel free to use and modify this code for personal or educational purposes.

This project was created as a simple demonstration of Python basics and CSV file handling.