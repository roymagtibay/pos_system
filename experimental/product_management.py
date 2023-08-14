import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from manage_item import AddItem
<<<<<<< Updated upstream
from database_manager import SalesCreateQuery
=======
from database_manager import InitTableQuery
from database_manager import ListItemQuery
>>>>>>> Stashed changes

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()


        self.initate_db_table()
        self.create_body()


    def initate_db_table(self):
        # creates table for db
        self.create_query = SalesCreateQuery()

        self.create_query.initiate_item_table()
        self.create_query.initiate_item_type_table()
        self.create_query.initiate_brand_table()
        self.create_query.initiate_sales_group_table()
        self.create_query.initiate_supplier_table()
        self.create_query.initiate_item_price_table()
        self.create_query.initiate_promo_table()
        # self.create_query.initiate_customer_table()
        # self.create_query.initiate_stocks_table()
        # self.create_query.initiate_item_sold_table()

        self.init_table.close()

    def open_add_item_window(self):
        self.add_item_window = AddItem()
        self.add_item_window.exec()


    def show_item_list_table(self):
        self.list_item = ListItemQuery()

    def create_body(self):
        self.layout = QGridLayout()

        self.add_item_button = QPushButton('ADD ITEM')
        self.add_item_button.clicked.connect(self.open_add_item_window)

        self.item_list_table = QTableWidget()
        self.item_list_table.setColumnCount(10)
        self.item_list_table.setHorizontalHeaderLabels(['Item name','Barcode','Item type','Brand','Supplier','Sales group','Cost','Discount','Sell price','Expire date'])

        self.layout.addWidget(self.add_item_button)
        self.layout.addWidget(self.item_list_table)

        self.setLayout(self.layout)


if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagement()
    window.show()
    sys.exit(pos_app.exec())