import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from manage_item import AddItem
from database_manager import InitTableQuery
from database_manager import ListItemQuery

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()

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


    def show_item_list_table(self):
        self.list_item = ListItemQuery()
        
        # item_name_data = self.list_item.retrieve_item_name_data() # has a data (item_name)
        # barcode_data = self.list_item.retrieve_barcode_data() # has a data (barcode)
        # expire_dt_data = self.list_item.retrieve_expire_dt_data() # has a data (expire_dt)
        # item_type_data = self.list_item.retrieve_item_type_data() # has a data (name)
        # brand_data = self.list_item.retrieve_brand_data() # has a data (name)
        # sales_group_data = self.list_item.retrieve_sales_group_data() # has a data (name)
        # supplier_data = self.list_item.retrieve_supplier_data() # has a data (name)
        # item_cost_data = self.list_item.retrieve_cost_data() # has a data (cost)
        # item_discount_data = self.list_item.retrieve_discount_data() # has a data (discount)
        # item_sell_price_data = self.list_item.retrieve_sell_price_data() # has a data (sell_price)

        

        # os.system('cls')
        # print('item name:', item_name_data)
        # print('barcode:', barcode_data)
        # print('expire date:', expire_dt_data)
        # print('item type:', item_type_data)
        # print('brand:', brand_data)
        # print('sales group:', sales_group_data)
        # print('supplier:', supplier_data)
        # print('cost:', item_cost_data)
        # print('discount:', item_discount_data)
        # print('sell price:', item_sell_price_data)

        item_data = self.list_item.retrieve_item_data()
        print(item_data)

        self.list_item.close()

        num_rows = len(item_data)

        self.item_list_table.setRowCount(num_rows)

        for row_idx, row_data in enumerate(item_data):
            self.edit_item_button = QPushButton('EDIT')
            self.item_list_table.setCellWidget(row_idx, 0, self.edit_item_button)

            for col_idx, col_data in enumerate(row_data):
                self.item_list_table.setItem(row_idx, col_idx + 1, QTableWidgetItem(str(col_data)))


    def create_body(self):
        self.layout = QGridLayout()

        self.add_item_button = QPushButton('ADD ITEM')
        self.add_item_button.clicked.connect(self.open_add_item_window)

        self.item_list_table = QTableWidget()
        self.item_list_table.setColumnCount(11)
        self.item_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.item_list_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.item_list_table.setHorizontalHeaderLabels(['','Item name','Barcode','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Expire date'])

        self.layout.addWidget(self.add_item_button)
        self.layout.addWidget(self.item_list_table)

        self.setLayout(self.layout)


if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagement()
    window.show()
    sys.exit(pos_app.exec())