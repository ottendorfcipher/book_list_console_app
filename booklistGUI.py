import sys
import csv
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                            QMessageBox, QFileDialog, QGroupBox, QFormLayout, QHeaderView)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

class BookManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.books = []
        self.initUI()
        
    def initUI(self):
        # Set up the main window
        self.setWindowTitle('Book Management System')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # ---- Left side with controls ----
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Form for adding a book
        add_book_group = QGroupBox("Add New Book")
        form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.author_first_name_input = QLineEdit()
        self.author_last_name_input = QLineEdit()
        self.price_input = QLineEdit()
        
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author First Name:", self.author_first_name_input)
        form_layout.addRow("Author Last Name:", self.author_last_name_input)
        form_layout.addRow("Price ($):", self.price_input)
        
        add_button = QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)
        form_layout.addRow("", add_button)
        
        add_book_group.setLayout(form_layout)
        left_layout.addWidget(add_book_group)
        
        # Export button
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        left_layout.addWidget(export_button)
        
        # About button
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        left_layout.addWidget(about_button)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)
        
        # ---- Right side with table view ----
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Table for showing books
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Title", "Author First Name", "Author Last Name", "Price"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        right_layout.addWidget(QLabel("<h2>Book Collection</h2>"))
        right_layout.addWidget(self.table)
        
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def add_book(self):
        title = self.title_input.text().strip()
        author_first_name = self.author_first_name_input.text().strip()
        author_last_name = self.author_last_name_input.text().strip()
        price_text = self.price_input.text().strip()
        
        # Validate inputs
        if not title:
            QMessageBox.warning(self, "Input Error", "Please enter a book title.")
            return
            
        if not author_first_name or not author_last_name:
            QMessageBox.warning(self, "Input Error", "Please enter the author's full name.")
            return
            
        try:
            price = float(price_text)
            if price < 0:
                QMessageBox.warning(self, "Input Error", "Price cannot be negative.")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid price.")
            return
            
        # Create book entry
        book = {
            'title': title,
            'author_first_name': author_first_name,
            'author_last_name': author_last_name,
            'price': price
        }
        
        # Add book to list
        self.books.append(book)
        
        # Clear inputs
        self.title_input.clear()
        self.author_first_name_input.clear()
        self.author_last_name_input.clear()
        self.price_input.clear()
        
        # Update table
        self.update_table()
        
        QMessageBox.information(self, "Success", f"Book '{title}' added successfully!")
        
    def update_table(self):
        self.table.setRowCount(0)  # Clear table
        
        for book in self.books:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(book['title']))
            self.table.setItem(row_position, 1, QTableWidgetItem(book['author_first_name']))
            self.table.setItem(row_position, 2, QTableWidgetItem(book['author_last_name']))
            self.table.setItem(row_position, 3, QTableWidgetItem(f"${book['price']:.2f}"))
            
    def export_to_csv(self):
        if not self.books:
            QMessageBox.information(self, "Export", "No books to export.")
            return
            
        # Open file dialog to get save location
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Books to CSV", "", "CSV Files (*.csv);;All Files (*)",
            options=options
        )
        
        if not filename:
            return  # User canceled the dialog
            
        # Add .csv extension if not provided
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['title', 'author_first_name', 'author_last_name', 'price'])
                writer.writeheader()
                writer.writerows(self.books)
            
            QMessageBox.information(
                self, "Export Successful", 
                f"Successfully exported {len(self.books)} books to:\n{os.path.abspath(filename)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error exporting to CSV: {str(e)}")
            
    def show_about(self):
        QMessageBox.about(
            self, "About Book Management System",
            "Book Management System\n\n"
            "A simple application to manage your book collection.\n\n"
            "Features:\n"
            "- Add books with title, author, and price\n"
            "- View your book collection\n"
            "- Export books to CSV format\n\n"
            "Created with PyQt5"
        )

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = BookManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
