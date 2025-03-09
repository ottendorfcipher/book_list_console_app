import pymongo
from bson import ObjectId
from PyQt5.QtWidgets import QMessageBox

class DatabaseHandler:
    def __init__(self, parent=None):
        self.parent = parent
        self.client = None
        self.books_collection = None
        self.connect_to_mongodb()
        
    def connect_to_mongodb(self):
        try:
            # Connect to MongoDB - update connection string as needed
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")
            self.db = self.client["book_management"]
            self.books_collection = self.db["books"]
            print("Connected to MongoDB successfully")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            if self.parent:
                QMessageBox.critical(self.parent, "Database Error", 
                                    f"Failed to connect to MongoDB: {str(e)}\n\nThe application will run without persistence.")
            self.books_collection = None
            
    def load_books(self):
        books = []
        if self.books_collection is not None:
            try:
                for book in self.books_collection.find():
                    # Convert MongoDB _id to string representation for internal tracking
                    book_dict = {'_id': str(book['_id'])}
                    
                    # Add all fields from the book document
                    for key, value in book.items():
                        if key != '_id':  # Skip the ObjectId as we've already converted it
                            book_dict[key] = value
                            
                    books.append(book_dict)
            except Exception as e:
                if self.parent:
                    QMessageBox.warning(self.parent, "Database Error", f"Error loading books: {str(e)}")
        return books
    
    def add_book(self, book):
        if self.books_collection is not None:
            try:
                result = self.books_collection.insert_one(book)
                # Return the MongoDB _id as string
                return str(result.inserted_id)
            except Exception as e:
                if self.parent:
                    QMessageBox.warning(self.parent, "Database Error", f"Error saving book: {str(e)}")
        return None
        
    def remove_book(self, book_id):
        if self.books_collection is not None:
            try:
                self.books_collection.delete_one({"_id": ObjectId(book_id)})
                return True
            except Exception as e:
                if self.parent:
                    QMessageBox.warning(self.parent, "Database Error", f"Error removing book: {str(e)}")
        return False
        
    def close_connection(self):
        if self.client:
            try:
                self.client.close()
                print("MongoDB connection closed")
            except Exception as e:
                print(f"Error closing MongoDB connection: {e}")
