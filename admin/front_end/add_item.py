import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from salesdb import SalesDBFunctions

class AddItem(QDialog):
    def __init__(self):
        super().__init__()

        self.create_content()

    

    def create_content(self):
        self.grid_layout = QGridLayout()

        self.sample_label = QLabel('PRODUCT')
        
        # primary information
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText('Item name')
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText('Barcode')

        # categorize
        self.item_type = QComboBox()
        self.item_type.setEditable(True)
        self.brand = QComboBox()
        self.brand.setEditable(True)
        self.supplier = QComboBox()
        self.supplier.setEditable(True)

        # pricing
        self.sales_group = QComboBox()
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')

        self.item_price = QLineEdit()
        self.item_price.setPlaceholderText('Price')

        # validity
        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate())

        self.effective_date = QDateEdit()
        self.effective_date.setCalendarPopup(True)
        self.effective_date.setDate(QDate.currentDate())

        self.track_inventory = QLabel('Track inventory?')
        self.option_y_radio_button = QRadioButton('Yes')
        self.option_y_radio_button.setChecked(True)
        self.option_y_radio_button.clicked.connect(lambda: self.inventory_option('Yes'))
        self.option_n_radio_button = QRadioButton('No')
        self.option_n_radio_button.clicked.connect(lambda: self.inventory_option('No'))

        self.on_hand = QLineEdit()
        self.on_hand.setPlaceholderText('On hand')
        self.available = QLineEdit()
        self.available.setPlaceholderText('Available')

        self.save_item_push_button = QPushButton('SAVE ITEM')

        self.grid_layout.addWidget(self.item_name, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.barcode, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.item_type, 2, 0, 1, 2)
        self.grid_layout.addWidget(self.brand, 3, 0, 1, 2)
        self.grid_layout.addWidget(self.supplier, 4, 0, 1, 2)
        self.grid_layout.addWidget(self.sales_group, 5, 0, 1, 2)
        self.grid_layout.addWidget(self.item_price, 6, 0, 1, 2)
        self.grid_layout.addWidget(self.expiry_date, 7, 0, 1, 2)
        self.grid_layout.addWidget(self.effective_date, 8, 0, 1, 2)
        self.grid_layout.addWidget(self.track_inventory, 9, 0, 1, 2)
        self.grid_layout.addWidget(self.option_y_radio_button, 10, 0)
        self.grid_layout.addWidget(self.option_n_radio_button, 10, 1)
        self.grid_layout.addWidget(self.on_hand, 11, 0, 1, 2)
        self.grid_layout.addWidget(self.available, 12, 0, 1, 2)
        self.grid_layout.addWidget(self.save_item_push_button, 13, 0, 1, 2)

        self.setLayout(self.grid_layout)

    def inventory_option(self, option):
        if option == 'No':
            self.on_hand.setEnabled(False)
            self.available.setEnabled(False)
        elif option == 'Yes':
            self.on_hand.setEnabled(True)
            self.available.setEnabled(True)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddItem()
    window.show()
    sys.exit(pos_app.exec())