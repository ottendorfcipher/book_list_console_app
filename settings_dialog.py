from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QFormLayout, QCheckBox, QPushButton, QLabel,
                             QLineEdit, QScrollArea, QWidget, QMessageBox)
from PyQt5.QtCore import Qt, QSettings
from about_dialog import AboutDialog

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.custom_fields = []
        self.load_custom_fields()
        self.initUI()

    def load_custom_fields(self):
        # Load saved custom fields from settings
        size = self.settings.beginReadArray("customFields")
        for i in range(size):
            self.settings.setArrayIndex(i)
            field_name = self.settings.value("name", "")
            required = self.settings.value("required", False, type=bool)
            self.custom_fields.append({"name": field_name, "required": required})
        self.settings.endArray()

    def save_custom_fields(self):
        # Save custom fields to settings
        self.settings.beginWriteArray("customFields")
        for i, field in enumerate(self.custom_fields):
            self.settings.setArrayIndex(i)
            self.settings.setValue("name", field["name"])
            self.settings.setValue("required", field["required"])
        self.settings.endArray()

    def initUI(self):
        self.setWindowTitle("Preferences")  # Changed from "Settings" to "Preferences"
        self.setGeometry(300, 300, 500, 500)
        
        main_layout = QVBoxLayout()
        
        # Create a scroll area for the settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        # Dark Mode option
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()
        
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setChecked(self.settings.value("darkMode", False, type=bool))
        self.dark_mode_checkbox.toggled.connect(self.on_dark_mode_toggled)
        appearance_layout.addWidget(self.dark_mode_checkbox)
        
        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)
        
        # Required fields
        required_fields_group = QGroupBox("Required Fields")
        required_fields_layout = QVBoxLayout()
        
        # Standard fields
        self.title_required = QCheckBox("Title")
        self.title_required.setChecked(self.settings.value("titleRequired", True, type=bool))
        self.title_required.toggled.connect(lambda checked: self.settings.setValue("titleRequired", checked))
        required_fields_layout.addWidget(self.title_required)
        
        self.author_required = QCheckBox("Author Name")
        self.author_required.setChecked(self.settings.value("authorRequired", False, type=bool))
        self.author_required.toggled.connect(lambda checked: self.settings.setValue("authorRequired", checked))
        required_fields_layout.addWidget(self.author_required)
        
        self.price_required = QCheckBox("Price")
        self.price_required.setChecked(self.settings.value("priceRequired", False, type=bool))
        self.price_required.toggled.connect(lambda checked: self.settings.setValue("priceRequired", checked))
        required_fields_layout.addWidget(self.price_required)
        
        # Add custom field checkboxes
        self.custom_field_checkboxes = []
        for field in self.custom_fields:
            checkbox = QCheckBox(field["name"])
            checkbox.setChecked(field["required"])
            checkbox.toggled.connect(self.create_required_toggle_handler(field))
            required_fields_layout.addWidget(checkbox)
            self.custom_field_checkboxes.append(checkbox)
        
        required_fields_group.setLayout(required_fields_layout)
        layout.addWidget(required_fields_group)
        
        # Custom fields management
        custom_fields_group = QGroupBox("Custom Fields")
        custom_fields_layout = QVBoxLayout()
        
        # Show existing custom fields
        if self.custom_fields:
            current_fields_label = QLabel("Current Custom Fields:")
            custom_fields_layout.addWidget(current_fields_label)
            
            for i, field in enumerate(self.custom_fields):
                field_layout = QHBoxLayout()
                field_layout.addWidget(QLabel(f"{i+1}. {field['name']}"))
                
                # Delete button
                delete_btn = QPushButton("Delete")
                delete_btn.setProperty("fieldIndex", i)
                delete_btn.clicked.connect(self.delete_custom_field)
                field_layout.addWidget(delete_btn)
                
                custom_fields_layout.addLayout(field_layout)
        
        # Add new custom field
        add_field_layout = QHBoxLayout()
        add_field_layout.addWidget(QLabel("New Field:"))
        self.new_field_input = QLineEdit()
        add_field_layout.addWidget(self.new_field_input)
        
        add_field_btn = QPushButton("Add Field")
        add_field_btn.clicked.connect(self.add_custom_field)
        add_field_layout.addWidget(add_field_btn)
        
        custom_fields_layout.addLayout(add_field_layout)
        custom_fields_group.setLayout(custom_fields_layout)
        layout.addWidget(custom_fields_group)
        
        # Set the scroll content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Buttons section at the bottom
        button_layout = QHBoxLayout()
        
        # About button
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        about_button.setFixedWidth(100)
        button_layout.addWidget(about_button)
        
        button_layout.addStretch()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setFixedWidth(100)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept_changes)
        ok_button.setFixedWidth(100)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def create_required_toggle_handler(self, field):
        """Creates a handler for toggling required status of custom fields"""
        def toggle_handler(checked):
            field["required"] = checked
        return toggle_handler
        
    def add_custom_field(self):
        field_name = self.new_field_input.text().strip()
        if not field_name:
            QMessageBox.warning(self, "Input Error", "Please enter a field name.")
            return
            
        # Check for duplicate field names
        if field_name.lower() in ["title", "author name", "price"] or \
           any(field["name"].lower() == field_name.lower() for field in self.custom_fields):
            QMessageBox.warning(self, "Input Error", f"Field '{field_name}' already exists.")
            return
            
        # Add the new field
        self.custom_fields.append({"name": field_name, "required": False})
        self.new_field_input.clear()
        
        # Refresh the dialog to show the new field
        self.save_custom_fields()
        self.reject()
        self.__init__(self.parent, self.settings)
        self.exec_()
        
    def delete_custom_field(self):
        sender = self.sender()
        index = sender.property("fieldIndex")
        
        if 0 <= index < len(self.custom_fields):
            self.custom_fields.pop(index)
            
            # Refresh the dialog to update the field list
            self.save_custom_fields()
            self.reject()
            self.__init__(self.parent, self.settings)
            self.exec_()
    
    def accept_changes(self):
        # Save custom fields with their required status
        for i, field in enumerate(self.custom_fields):
            if i < len(self.custom_field_checkboxes):
                field["required"] = self.custom_field_checkboxes[i].isChecked()
        
        self.save_custom_fields()
        self.accept()
    
    def on_dark_mode_toggled(self, checked):
        self.settings.setValue("darkMode", checked)
        self.parent.apply_theme()
        self.apply_dialog_theme(checked)
        
    def apply_dialog_theme(self, dark_mode=None):
        """Apply theme to the dialog"""
        if dark_mode is None:
            dark_mode = self.settings.value("darkMode", False, type=bool)
            
        if dark_mode:
            self.setStyleSheet("""
                QDialog { background-color: #333; color: white; }
                QGroupBox { 
                    border: 1px solid #555; 
                    color: white; 
                    margin-top: 1.5ex;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 5px;
                }
                QLabel { color: white; }
                QLineEdit { 
                    background-color: #444; 
                    color: white; 
                    border: 1px solid #555; 
                    padding: 5px;
                }
                QPushButton { 
                    background-color: #444; 
                    color: white; 
                    border: 1px solid #555; 
                    padding: 5px;
                    min-height: 25px;
                }
                QPushButton:hover { background-color: #555; }
                QCheckBox { 
                    color: white; 
                    spacing: 5px;
                }
                QCheckBox::indicator {
                    width: 13px;
                    height: 13px;
                    border: 1px solid #555;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078d7;
                }
                QScrollArea { 
                    background-color: #333; 
                    border: 1px solid #555;
                }
                QScrollBar:vertical {
                    border: none;
                    background: #444;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #666;
                    min-height: 20px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    min-height: 25px;
                    padding: 5px;
                }
            """)
    
    def show_about(self):
        dark_mode = self.settings.value("darkMode", False, type=bool)
        about_dialog = AboutDialog(self, dark_mode)
        about_dialog.exec_()
        
    def showEvent(self, event):
        """Apply theme when dialog is shown"""
        super().showEvent(event)
        dark_mode = self.settings.value("darkMode", False, type=bool)
        self.apply_dialog_theme(dark_mode)
