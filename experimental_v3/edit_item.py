import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from db_manager import *

class EditItem(QDialog):
    data_stored = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.store_query = StoreData()
        self.retrieve_query = RetrieveId()

        self.create_body()

    def create_body(self):
        self.layout = QGridLayout()

    # declare widgets
        item_name_field = QComboBox()
        barcode_field = QLineEdit()
        expire_dt_field = QDateEdit()
        item_type_field = QComboBox()
        brand_field = QComboBox()
        sales_group_field = QComboBox()
        supplier_field = QComboBox()
        cost_field = QLineEdit()
        discount_field = QLineEdit()
        sell_price_field = QLineEdit()
        effective_dt_field = QDateEdit()
        save_button = QPushButton('SAVE ITEM')

    # store widgets to the QGridLayout
        self.layout.addWidget(item_name_field)
        self.layout.addWidget(barcode_field)
        self.layout.addWidget(expire_dt_field)
        self.layout.addWidget(item_type_field)
        self.layout.addWidget(brand_field)
        self.layout.addWidget(sales_group_field)
        self.layout.addWidget(supplier_field)
        self.layout.addWidget(cost_field)
        self.layout.addWidget(discount_field)
        self.layout.addWidget(sell_price_field)
        self.layout.addWidget(effective_dt_field)
        self.layout.addWidget(save_button)
        
        self.setLayout(self.layout)


if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = EditItem()
    window.show()
    sys.exit(pos_app.exec())