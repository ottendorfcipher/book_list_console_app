from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AboutDialog(QDialog):
    def __init__(self, parent=None, dark_mode=False):
        super().__init__(parent)
        self.setWindowTitle("About Book Management System")
        self.setGeometry(300, 300, 450, 350)
        self.dark_mode = dark_mode
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Book Management System")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Create scrollable area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Description
        description = QLabel(
            "A simple application to manage your book collection.\n\n"
            "Features:\n"
            "• Add books with title, author, and price\n"
            "• Add custom fields to track additional information\n"
            "• Remove books by selecting them from the table\n"
            "• View your book collection\n"
            "• Export books to CSV, JSON, or Excel format\n"
            "• MongoDB storage for persistence\n"
            "• Dark mode and customizable required fields\n\n"
            "This application is built with PyQt5 and MongoDB.\n\n"
            "Version: 0.0.3\n"
            "© 2025 Book Management System, OttendorfCipher, Built with assistance from Anthropic Claude 3.7 Sonnet AI"
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        scroll_layout.addWidget(description)
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
        # Apply theme if dark mode
        if self.dark_mode:
            self.setStyleSheet("""
                QDialog { background-color: #333; color: white; }
                QLabel { color: white; }
                QScrollArea { background-color: #333; border: 1px solid #555; }
                QWidget { background-color: #333; }
                QPushButton { 
                    background-color: #444; 
                    color: white; 
                    padding: 6px; 
                    border: 1px solid #555; 
                }
                QPushButton:hover { background-color: #555; }
            """)
