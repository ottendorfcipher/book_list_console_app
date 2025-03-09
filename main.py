import sys
from PyQt5.QtWidgets import QApplication
from book_management_app import BookManagementApp

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = BookManagementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
