import os
import csv
import json
import pandas as pd
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                            QMessageBox, QGroupBox, QFormLayout, QHeaderView,
                            QAbstractItemView, QMenuBar, QMenu, QAction, QApplication)
from PyQt5.QtCore import Qt, QSettings, QTimer
from settings_dialog import SettingsDialog
from database_handler import DatabaseHandler
from ui_components import (create_confirmation_dialog, get_dark_palette, 
                         get_delete_button_style, ExportDialog, get_preferences_button_style)
from about_dialog import AboutDialog

class BookManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize settings
        self.settings = QSettings("MyCompany", "BookManagementSystem")
        
        # Initialize books list
        self.books = []
        
        # Initialize custom fields dictionary
        self.custom_fields = []
        self.load_custom_fields()
        
        # Connect to database
        self.db_handler = DatabaseHandler(self)
        
        # Load books from database
        self.load_books_from_db()
        
        # Initialize UI
        self.initUI()
        
        # Apply theme based on settings after UI is initialized
        QTimer.singleShot(100, self.apply_theme)

    def load_custom_fields(self):
        # Load saved custom fields from settings
        self.custom_fields = []
        size = self.settings.beginReadArray("customFields")
        for i in range(size):
            self.settings.setArrayIndex(i)
            field_name = self.settings.value("name", "")
            required = self.settings.value("required", False, type=bool)
            self.custom_fields.append({"name": field_name, "required": required})
        self.settings.endArray()

    def load_books_from_db(self):
        self.books = self.db_handler.load_books()

    def initUI(self):
        # Set up the main window
        self.setWindowTitle('Book Management System')
        self.setGeometry(100, 100, 900, 600)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # ---- Left side with controls ----
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Form for adding a book
        add_book_group = QGroupBox("Add New Book")
        self.form_layout = QFormLayout()  # Store as instance variable for later access
        
        # Standard fields
        self.title_input = QLineEdit()
        self.author_name_input = QLineEdit()
        self.price_input = QLineEdit()
        
        # Add labels with placeholders for required indicators
        self.title_label = QLabel("Title:")
        self.author_label = QLabel("Author Name:")
        self.price_label = QLabel("Price ($):")
        
        self.form_layout.addRow(self.title_label, self.title_input)
        self.form_layout.addRow(self.author_label, self.author_name_input)
        self.form_layout.addRow(self.price_label, self.price_input)
        
        # Add custom field inputs - add ALL custom fields regardless of required status
        self.custom_field_inputs = {}
        self.custom_field_labels = {}
        
        for field in self.custom_fields:
            input_field = QLineEdit()
            label = QLabel(f"{field['name']}:")
            self.form_layout.addRow(label, input_field)
            self.custom_field_inputs[field['name']] = input_field
            self.custom_field_labels[field['name']] = label
        
        add_button = QPushButton("Add Book")
        add_button.clicked.connect(self.add_book)
        self.form_layout.addRow("", add_button)
        
        add_book_group.setLayout(self.form_layout)
        left_layout.addWidget(add_book_group)
        
        # Export button
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_books)
        left_layout.addWidget(export_button)
        
        # Preferences button - Blue primary color
        preferences_button = QPushButton("Preferences")
        preferences_button.clicked.connect(self.show_settings)
        preferences_button.setStyleSheet(get_preferences_button_style())
        left_layout.addWidget(preferences_button)
        
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)
        
        # ---- Right side with table view ----
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Table for showing books
        self.table = QTableWidget()
        self.setup_table()
        
        right_layout.addWidget(QLabel("<h2>Book Collection</h2>"))
        right_layout.addWidget(self.table)
        
        # Add remove button at the bottom right underneath the book list
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # This pushes the button to the right
        
        # Create the remove button
        self.remove_button = QPushButton("Remove Selected Book")
        self.remove_button.clicked.connect(self.remove_selected_book)
        
        # Set the button style (red when enabled)
        self.remove_button.setStyleSheet(get_delete_button_style())
        
        # Initially disable the button since no book is selected at startup
        self.remove_button.setEnabled(False)
        
        button_layout.addWidget(self.remove_button)
        right_layout.addLayout(button_layout)
        
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Update required field indicators
        self.update_required_field_indicators()
        
        # Update the table with books
        self.update_table()
        
        # Connect table selection signal after initialization
        QTimer.singleShot(100, self.connect_table_signals)
    
    def setup_table(self):
        """Set up the table structure based on standard and custom fields"""
        # Calculate column count (title, author, price + custom fields)
        column_count = 3 + len(self.custom_fields)
        self.table.setColumnCount(column_count)
        
        # Create headers
        headers = ["Title", "Author Name", "Price"]
        headers.extend([field["name"] for field in self.custom_fields])
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set stretch for columns
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # Title
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Author
        
        # Set fixed width for price column
        if self.table.columnCount() > 2:
            self.table.setColumnWidth(2, 100)  # Price column
        
        # Set remaining columns (custom fields) to reasonable widths
        for i in range(3, column_count):
            self.table.setColumnWidth(i, 150)
        
        # Enable row selection
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
    
    def connect_table_signals(self):
        """Connect signals after initialization to ensure models exist"""
        if self.table.selectionModel():
            self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        export_action = QAction('Export', self)
        export_action.triggered.connect(self.export_books)
        file_menu.addAction(export_action)
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu - Change to "Preferences"
        preferences_menu = menubar.addMenu('Preferences')
        
        preferences_action = QAction('Preferences', self)
        preferences_action.triggered.connect(self.show_settings)
        preferences_menu.addAction(preferences_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_settings(self):
        settings_dialog = SettingsDialog(self, self.settings)
        if settings_dialog.exec_():
            # Reload custom fields
            self.load_custom_fields()
            
            # Reinitialize UI to show updated custom fields
            self.recreate_ui()
            
            # Update required field indicators
            self.update_required_field_indicators()
    
    def recreate_ui(self):
        """Recreate the UI to reflect changes in custom fields"""
        # Store current central widget to delete later
        old_central = self.centralWidget()
        
        # Initialize new UI
        self.initUI()
        
        # Delete old widget to free resources
        if old_central:
            old_central.deleteLater()
    
    def update_required_field_indicators(self):
        """Update field labels to indicate required fields with asterisks"""
        title_required = self.settings.value("titleRequired", True, type=bool)
        author_required = self.settings.value("authorRequired", False, type=bool)
        price_required = self.settings.value("priceRequired", False, type=bool)
        
        # Update the labels directly
        self.title_label.setText("Title:" + (" *" if title_required else ""))
        self.author_label.setText("Author Name:" + (" *" if author_required else ""))
        self.price_label.setText("Price ($):" + (" *" if price_required else ""))
        
        # Update custom field labels
        for field in self.custom_fields:
            if field["name"] in self.custom_field_labels:
                label = self.custom_field_labels[field["name"]]
                label.setText(f"{field['name']}:" + (" *" if field["required"] else ""))
        
    def apply_theme(self):
        """Apply dark or light theme based on settings"""
        dark_mode = self.settings.value("darkMode", False, type=bool)
        
        if dark_mode:
            # Set dark theme
            app = QApplication.instance()
            app.setPalette(get_dark_palette())
            
            # Adjust table colors for better readability in dark mode
            self.table.setStyleSheet("""
                QTableWidget {
                    background-color: #1e1e1e;
                    color: white;
                    gridline-color: #444;
                }
                QHeaderView::section {
                    background-color: #333;
                    color: white;
                    border: 1px solid #444;
                }
                QTableWidget::item:selected {
                    background-color: #0078d7;
                }
            """)
            
            # Keep red color for the Remove button
            self.remove_button.setStyleSheet(get_delete_button_style())
            
            # Keep blue color for the Preferences button
            for widget in self.findChildren(QPushButton):
                if widget.text() == "Preferences":
                    widget.setStyleSheet(get_preferences_button_style())
        else:
            # Reset to default light theme
            app = QApplication.instance()
            app.setPalette(app.style().standardPalette())
            
            # Reset table style
            self.table.setStyleSheet("")
            
            # Reset button to original style, but keep it red for the Remove button
            self.remove_button.setStyleSheet(get_delete_button_style())
            
            # Keep blue color for the Preferences button
            for widget in self.findChildren(QPushButton):
                if widget.text() == "Preferences":
                    widget.setStyleSheet(get_preferences_button_style())
        
    def on_selection_changed(self, selected, deselected):
        """Enable remove button only when a row is selected"""
        self.remove_button.setEnabled(len(self.table.selectionModel().selectedRows()) > 0)
        
    def add_book(self):
        """Add a new book to the collection"""
        title = self.title_input.text().strip()
        author_name = self.author_name_input.text().strip()
        price_text = self.price_input.text().strip()
        
        # Check required fields
        title_required = self.settings.value("titleRequired", True, type=bool)
        author_required = self.settings.value("authorRequired", False, type=bool)
        price_required = self.settings.value("priceRequired", False, type=bool)
        
        # Validate inputs based on required fields
        error_messages = []
        
        if title_required and not title:
            error_messages.append("Title is required.")
            
        if author_required and not author_name:
            error_messages.append("Author Name is required.")
            
        if price_required and not price_text:
            error_messages.append("Price is required.")
        
        # Check custom field requirements
        for field in self.custom_fields:
            field_name = field["name"]
            if field_name in self.custom_field_inputs:
                field_value = self.custom_field_inputs[field_name].text().strip()
                if field["required"] and not field_value:
                    error_messages.append(f"{field_name} is required.")
        
        # Show errors if any required fields are missing
        if error_messages:
            QMessageBox.warning(self, "Input Error", "\n".join(error_messages))
            return
            
        # Validate price if provided
        if price_text:
            try:
                price = float(price_text)
                if price < 0:
                    QMessageBox.warning(self, "Input Error", "Price cannot be negative.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please enter a valid price.")
                return
        else:
            price = 0.0  # Default price if not provided and not required
            
        # Create book entry
        book = {
            'title': title,
            'author_name': author_name,
            'price': price
        }
        
        # Add custom field values
        for field in self.custom_fields:
            field_name = field["name"]
            if field_name in self.custom_field_inputs:
                field_value = self.custom_field_inputs[field_name].text().strip()
                book[field_name] = field_value
        
        # Add book to MongoDB and get ID
        book_id = self.db_handler.add_book(book)
        if book_id:
            book['_id'] = book_id
        
        # Add book to list
        self.books.append(book)
        
        # Clear inputs
        self.title_input.clear()
        self.author_name_input.clear()
        self.price_input.clear()
        
        # Clear custom field inputs
        for input_field in self.custom_field_inputs.values():
            input_field.clear()
        
        # Update table
        self.update_table()
    
    def remove_selected_book(self):
        """Remove the selected book from the collection"""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if not selected_rows:
            # This should not happen as button should be disabled, but keep as safeguard
            QMessageBox.warning(self, "Selection Error", "Please select a book to remove.")
            return
        
        row_index = selected_rows[0].row()
        if row_index < 0 or row_index >= len(self.books):
            return
            
        book = self.books[row_index]
        
        # Create custom confirmation dialog with red Yes button
        dark_mode = self.settings.value("darkMode", False, type=bool)
        msg_box = create_confirmation_dialog(
            self, 
            'Confirm Removal', 
            f"Are you sure you want to remove '{book['title']}' by {book['author_name']}?",
            dark_mode
        )
        
        msg_box.exec_()
        
        # Check which button was clicked
        if msg_box.clickedButton() == msg_box.buttons()[0]:  # Yes button is first
            # Delete from database if available
            if '_id' in book:
                self.db_handler.remove_book(book['_id'])
            
            # Remove from local list
            self.books.pop(row_index)
            
            # Update table
            self.update_table()
            
            QMessageBox.information(self, "Success", "Book removed successfully!")
    
    def update_table(self):
        """Update the table with current book data"""
        # Safely disconnect selection signal if connected
        try:
            if self.table.selectionModel():
                self.table.selectionModel().selectionChanged.disconnect(self.on_selection_changed)
        except TypeError:
            # Signal wasn't connected, which is fine
            pass
        
        self.table.setRowCount(0)  # Clear table
        
        for book in self.books:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            # Add standard fields
            self.table.setItem(row_position, 0, QTableWidgetItem(book.get('title', '')))
            self.table.setItem(row_position, 1, QTableWidgetItem(book.get('author_name', '')))
            self.table.setItem(row_position, 2, QTableWidgetItem(f"${book.get('price', 0):.2f}"))
            
            # Add custom fields
            for col_idx, field in enumerate(self.custom_fields, start=3):
                field_name = field["name"]
                value = book.get(field_name, '')
                self.table.setItem(row_position, col_idx, QTableWidgetItem(str(value)))
        
        # Reconnect the selection signal
        QTimer.singleShot(0, self.connect_table_signals)
        
        # Ensure the remove button is properly disabled if no row is selected
        self.remove_button.setEnabled(False)
            
    def export_books(self):
        """Export the book collection"""
        if not self.books:
            QMessageBox.information(self, "Export", "No books to export.")
            return
            
        # Show export options dialog
        dark_mode = self.settings.value("darkMode", False, type=bool)
        export_dialog = ExportDialog(self, dark_mode)
        if not export_dialog.exec_():
            return  # User canceled
        
        # Get export format and file path
        export_format = export_dialog.selected_format
        file_path = export_dialog.file_path
        
        if not file_path:
            return
        
        try:
            # All book fields except MongoDB ID
            export_fields = ['title', 'author_name', 'price']
            export_fields.extend([field["name"] for field in self.custom_fields])
            
            if export_format == 'csv':
                self.export_to_csv(file_path, export_fields)
            elif export_format == 'json':
                self.export_to_json(file_path, export_fields)
            else:  # xlsx
                self.export_to_excel(file_path, export_fields)
            
            QMessageBox.information(
                self, "Export Successful", 
                f"Successfully exported {len(self.books)} books to:\n{os.path.abspath(file_path)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Error exporting books: {str(e)}")
    
    def export_to_csv(self, file_path, fields):
        """Export the book collection to a CSV file"""
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            
            # Write each book but exclude _id field
            for book in self.books:
                row = {}
                for field in fields:
                    row[field] = book.get(field, '')
                writer.writerow(row)
    
    def export_to_json(self, file_path, fields):
        """Export the book collection to a JSON file"""
        export_data = []
        
        for book in self.books:
            book_data = {}
            for field in fields:
                book_data[field] = book.get(field, '')
            export_data.append(book_data)
            
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(export_data, file, indent=4)
    
    def export_to_excel(self, file_path, fields):
        """Export the book collection to an Excel file"""
        # Create a dataframe with all books
        data = []
        for book in self.books:
            row = {}
            for field in fields:
                row[field] = book.get(field, '')
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
            
    def show_about(self):
        """Show information about the application"""
        dark_mode = self.settings.value("darkMode", False, type=bool)
        about_dialog = AboutDialog(self, dark_mode)
        about_dialog.exec_()
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Close MongoDB connection
        self.db_handler.close_connection()
        event.accept()
