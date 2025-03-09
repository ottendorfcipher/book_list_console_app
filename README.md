# Book Management System

A desktop application for managing your book collection with MongoDB integration, custom fields, dark mode, and multiple export formats.

## Features

- Add, view, and remove books in your collection
- Store book details (title, author, price)
- Create custom fields for additional information
- MongoDB database integration for persistent storage
- Export your collection to CSV, JSON, or Excel format
- Dark mode support
- Customizable required fields
- Simple and intuitive user interface
  
## Requirements

- Python 3.6+
- PyQt5
- pymongo
- pandas (for Excel export)

## Installation

1. Clone the repository or download the source code

`git clone https://github.com/yourusername/book-management-system.git`
`cd book-management-system`

3. Install the required dependencies
`pip install PyQt5 pymongo pandas openpyxl`

4. Make sure MongoDB is installed and running on your system
- If you haven't installed MongoDB yet, follow the [official installation guide](https://docs.mongodb.com/manual/installation/)
- By default, the application connects to MongoDB at `mongodb://localhost:27017/`
- If your MongoDB setup is different, update the connection string in `database_handler.py`

## Running the Application

Execute the main script to start the application:

`python main.py`

If MongoDB is not available, the application will still run, but without persistent storage.

## Project Structure

- `main.py` - Application entry point
- `book_management_app.py` - Main application window and logic
- `database_handler.py` - MongoDB database operations
- `settings_dialog.py` - Application settings management
- `about_dialog.py` - About information dialog
- `ui_components.py` - Reusable UI components and styles

## Usage

### Adding Books
1. Fill in the book information in the form on the left panel
2. Click "Add Book"

### Adding Custom Fields
1. Go to Preferences
2. In the "Custom Fields" section, enter a new field name
3. Click "Add Field"
4. The new field will appear in the book form and table

### Setting Required Fields
1. Go to Preferences
2. In the "Required Fields" section, check the fields that should be required
3. Required fields will be marked with an asterisk (*) in the form

### Removing Books
1. Select a book from the table
2. Click the "Remove Selected Book" button
3. Confirm deletion

### Exporting Your Collection
1. Click the "Export" button
2. Choose an export format (CSV, JSON, or Excel)
3. Select a location to save the file

### Dark Mode
1. Go to Preferences
2. Check the "Dark Mode" option to enable a darker theme

## License

This project is licensed under the MIT License - see the LICENSE file for details.
