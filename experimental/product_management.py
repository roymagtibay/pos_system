import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from manage_item import AddItem
from database_manager import InitTableQuery

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()


        self.initate_db_table()
        self.create_body()


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

    def show_add_item_window(self):
        self.add_item_window = AddItem()
        self.add_item_window.exec()


    def create_body(self):
        self.layout = QGridLayout()

        


        self.add_item_button = QPushButton('ADD ITEM')
        self.add_item_button.clicked.connect(self.show_add_item_window)

        self.item_list_table = QTableWidget()

        self.layout.addWidget(self.add_item_button)
        self.layout.addWidget(self.item_list_table)

        self.setLayout(self.layout)


if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagement()
    window.show()
    sys.exit(pos_app.exec())