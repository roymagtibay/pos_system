import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from manage_item import AddItem
from manage_item import EditItem
from database_manager import InitTableQuery
from database_manager import ListItemQuery
from database_manager import DeleteItemQuery

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Product Management')
        self.setGeometry(300, 100, 1000, 500)

        self.create_body()
        self.initate_db_table()
        self.show_item_list_table()
        

    def initate_db_table(self):
        # creates table for db
        self.init_table = InitTableQuery()

        self.init_table.initiate_item_table()
        self.init_table.initiate_item_type_table()
        self.init_table.initiate_brand_table()
        self.init_table.initiate_sales_group_table()
        self.init_table.initiate_supplier_table()
        self.init_table.initiate_item_price_table()
        self.init_table.initiate_promo_table()
        # self.init_table.initiate_customer_table()
        # self.init_table.initiate_stocks_table()
        # self.init_table.initiate_item_sold_table()

        self.init_table.close()

    def open_add_item_window(self):
        self.add_item_window = AddItem()
        self.add_item_window.data_stored.connect(self.show_item_list_table)
        self.add_item_window.exec()

    def open_edit_item_window(self, row, item):
        self.edit_item_window = EditItem(row, item)
        self.edit_item_window.data_stored.connect(self.show_item_list_table)
        self.edit_item_window.exec()

    def show_item_list_table(self):
        self.list_item = ListItemQuery()

        item_data = self.list_item.retrieve_item_data()
        print(item_data)

        self.item_list_table.setRowCount(len(item_data))


        for row_index, row_value in enumerate(item_data):
            print('\n')
            for col_index, cell_value in enumerate(row_value):
                self.item_list_table.setItem(row_index, col_index + 1, QTableWidgetItem(str(cell_value)))
                print(cell_value, end=', ')
            
            self.edit_item_button = QPushButton('EDIT')
            self.edit_item_button.clicked.connect(lambda row=row_index, item=row_value: self.open_edit_item_window(row, item))
            self.delete_item_button = QPushButton('DELETE')

            # Check if the cell value in the third column is 'Unknown'
            if row_value[2] == 'unk':
                self.item_list_table.setCellWidget(row_index, 0, self.delete_item_button)
                self.item_list_table.setCellWidget(row_index, 1, None)  # Clear Edit button
            else:
                self.item_list_table.setCellWidget(row_index, 0, self.edit_item_button)
                self.item_list_table.setCellWidget(row_index, 1, None)

            
            # self.edit_item_button = QPushButton('EDIT')
            # self.edit_item_button.clicked.connect(lambda row=row_index, item=row_data: self.open_edit_item_window(row, item))
            # self.item_list_table.setCellWidget(row_index, 0, self.edit_item_button)

        self.list_item.close()

    def create_body(self):
        self.layout = QGridLayout()

        self.add_item_button = QPushButton('ADD ITEM')
        self.add_item_button.clicked.connect(self.open_add_item_window)

        self.item_list_table = QTableWidget()
        self.item_list_table.setColumnCount(12)
        self.item_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.item_list_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.item_list_table.setHorizontalHeaderLabels(['','Item name','Barcode','Expire date','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Effective Date'])

        self.layout.addWidget(self.add_item_button)
        self.layout.addWidget(self.item_list_table)

        self.setLayout(self.layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagement()
    window.show()
    sys.exit(pos_app.exec())