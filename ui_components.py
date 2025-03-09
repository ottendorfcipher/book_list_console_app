from PyQt5.QtWidgets import (QMessageBox, QPushButton, QDialog, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QFileDialog)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

def create_confirmation_dialog(parent, title, message, dark_mode=False):
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Question)
    
    # Create the buttons
    yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
    no_button = msg_box.addButton("No", QMessageBox.NoRole)
    
    # Style the Yes button to be red
    yes_button.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold;")
    
    # Apply dark mode to dialog if needed
    if dark_mode:
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #333;
                color: white;
            }
            QLabel {
                color: white;
            }
        """)
    
    return msg_box
    
def get_dark_palette():
    palette = QPalette()
    
    # Set dark color scheme
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    
    return palette

def get_delete_button_style():
    # Removed font-weight: bold from the enabled state
    return """
        QPushButton:enabled { 
            background-color: #d9534f; 
            color: white;
        }
        QPushButton:disabled { 
            background-color: #cccccc; 
            color: #666666;
        }
    """

def get_preferences_button_style():
    # Blue primary button
    return """
        QPushButton { 
            background-color: #0078d7; 
            color: white;
            min-height: 25px;
            padding: 5px;
        }
        QPushButton:hover { 
            background-color: #0086ef; 
        }
    """

class ExportDialog(QDialog):
    def __init__(self, parent=None, dark_mode=False):
        super().__init__(parent)
        self.parent = parent
        self.dark_mode = dark_mode
        self.selected_format = "csv"
        self.file_path = ""
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Export Options")
        self.setGeometry(300, 300, 400, 150)
        
        layout = QVBoxLayout()
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Export Format:"))
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV (.csv)", "JSON (.json)", "Excel (.xlsx)"])
        format_layout.addWidget(self.format_combo)
        
        layout.addLayout(format_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setFixedWidth(100)
        
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.on_export_clicked)
        self.export_button.setFixedWidth(100)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Apply theme if in dark mode
        if self.dark_mode:
            self.setStyleSheet("""
                QDialog { background-color: #333; color: white; }
                QLabel { color: white; }
                QComboBox { 
                    background-color: #444; 
                    color: white; 
                    border: 1px solid #555; 
                    padding: 5px;
                }
                QComboBox::drop-down { 
                    border: 0px; 
                    background-color: #666;
                }
                QComboBox QAbstractItemView { 
                    background-color: #444; 
                    color: white;
                    selection-background-color: #666;
                }
                QPushButton { 
                    background-color: #444; 
                    color: white; 
                    border: 1px solid #555;
                    padding: 5px;
                    min-height: 25px;
                }
                QPushButton:hover { background-color: #555; }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    min-height: 25px;
                    padding: 5px;
                }
            """)
    def on_export_clicked(self):
        # Get selected format
        selected_text = self.format_combo.currentText()
        if "CSV" in selected_text:
            self.selected_format = "csv"
            file_filter = "CSV Files (*.csv)"
            default_ext = ".csv"
        elif "JSON" in selected_text:
            self.selected_format = "json"
            file_filter = "JSON Files (*.json)"
            default_ext = ".json"
        else:  # Excel
            self.selected_format = "xlsx"
            file_filter = "Excel Files (*.xlsx)"
            default_ext = ".xlsx"
        
        # Get save location
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Books", "", f"{file_filter};;All Files (*)",
            options=options
        )
        
        if file_path:
            # Add extension if not provided
            if not file_path.endswith(default_ext):
                file_path += default_ext
                
            self.file_path = file_path
            self.accept()
        # If no file path was selected, do nothing and keep dialog open

