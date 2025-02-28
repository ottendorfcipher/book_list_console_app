import csv
import os

def display_menu():
    """Display the main menu options."""
    print("\n--- Book Management System ---")
    print("1. Add a book")
    print("2. View all books")
    print("3. Export to CSV")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def add_book(books):
    """Add a new book to the collection."""
    print("\n--- Add a New Book ---")
    
    title = input("Enter book title: ")
    
    author_first_name = input("Enter author's first name: ")
    author_last_name = input("Enter author's last name: ")
    
    # Validate price input
    while True:
        try:
            price = float(input("Enter book price: $"))
            if price < 0:
                print("Price cannot be negative. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid price. Please enter a number.")
    
    book = {
        'title': title,
        'author_first_name': author_first_name,
        'author_last_name': author_last_name,
        'price': price
    }
    
    books.append(book)
    print(f"\nBook '{title}' added successfully!")
    return books

def view_books(books):
    """Display all books in the collection."""
    if not books:
        print("\nNo books in the collection yet.")
        return
        
    print("\n--- Book Collection ---")
    print(f"{'Title':<30} {'Author':<30} {'Price':<10}")
    print("-" * 70)
    
    for book in books:
        author_full = f"{book['author_first_name']} {book['author_last_name']}"
        price_formatted = f"${book['price']:.2f}"
        print(f"{book['title']:<30} {author_full:<30} {price_formatted:<10}")

def export_to_csv(books):
    """Export the book collection to a CSV file."""
    if not books:
        print("\nNo books to export.")
        return
        
    filename = input("\nEnter filename for CSV export (default: books.csv): ") or "books.csv"
    
    # Add .csv extension if not provided
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['title', 'author_first_name', 'author_last_name', 'price'])
            writer.writeheader()
            writer.writerows(books)
        
        print(f"\nSuccessfully exported {len(books)} books to {filename}")
        print(f"File saved at: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"\nError exporting to CSV: {e}")

def main():
    """Main application function."""
    books = []
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            books = add_book(books)
        elif choice == '2':
            view_books(books)
        elif choice == '3':
            export_to_csv(books)
        elif choice == '4':
            print("\nThank you for using the Book Management System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
