import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

# allows importing files from different path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db_manager.db_manager import CreateDatabaseTable
from item_management.add_item import AddItem

class ItemManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.create_database_table = CreateDatabaseTable()

        self.setWindowTitle('Item Management')
        self.setGeometry(100,100,1000,500)
        

        self.create_body()

    def open_add_item_window(self):
        self.add_item_data = AddItem()
        self.add_item_data.exec()
        
    # def show_item_list(self):

    def create_body(self):
        self.create_database_table.create_database_table()
        
        self.body_layout = QGridLayout()
        
        add_item_button = QPushButton('ADD ITEM')
        add_item_button.clicked.connect(self.open_add_item_window)
        filter_entry_field = QLineEdit()
        filter_entry_field.setPlaceholderText('Filter item by ...')

        item_list_table = QTableWidget()
        

        self.body_layout.addWidget(add_item_button,0,1)
        self.body_layout.addWidget(filter_entry_field,0,0)
        self.body_layout.addWidget(item_list_table,1,0,1,2)
        self.setLayout(self.body_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagement()
    window.show()
    sys.exit(pos_app.exec())

        
