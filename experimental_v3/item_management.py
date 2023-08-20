import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from db_manager import *
from add_item import *
from edit_item import *

class ItemManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Item Management')
        self.setGeometry(1000,100,300,300)

        self.retrieve_data = RetrieveData() # --connected to 'display_list_item_table()'
        self.add_item = AddItem()
        self.edit_item = EditItem()

        self.create_body()

    def open_add_item_window(self):
        self.add_item.data_stored.connect(self.display_list_item_table)
        self.add_item.exec()

    def open_edit_item_window(self, row, item):
        
        self.edit_item.exec()

    def display_list_item_table(self):
        all_item_data = self.retrieve_data.all_item_data()

        self.list_item_table.setRowCount(len(all_item_data))

        for row_index, row_value in enumerate(all_item_data):
            for col_index, col_value in enumerate(row_value):
                self.list_item_table.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
    
            self.edit_item_button = QPushButton('EDIT')
            self.list_item_table.setCellWidget(row_index, 0, self.edit_item_button)
            self.edit_item_button.clicked.connect(lambda row=row_index, item=row_value: self.open_edit_item_window(row, item))

    def create_body(self):
        self.layout = QGridLayout()

        self.list_item_table = QTableWidget()
        filter_item_field = QLineEdit()
        add_item_button = QPushButton('ADD ITEM')

        self.list_item_table.setColumnCount(12)
        self.list_item_table.setHorizontalHeaderLabels(['','Item name','Barcode','Expire date','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Effective date'])

        add_item_button.clicked.connect(self.open_add_item_window)
        
        self.display_list_item_table()
        
        self.layout.addWidget(filter_item_field,0,0)
        self.layout.addWidget(add_item_button,0,1)
        self.layout.addWidget(self.list_item_table,1,0,1,2)

        self.setLayout(self.layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagement()
    window.show()
    sys.exit(pos_app.exec())