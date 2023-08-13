import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from salesdb import SalesDBFunctions

class EditItem(QDialog):
    data_saved = pyqtSignal()

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

        self.item_cost = QLineEdit()
        self.item_cost.setPlaceholderText('Cost')
        self.item_discount = QLineEdit()
        self.item_discount.setPlaceholderText('Discount')
        self.item_sell_price = QLineEdit()
        self.item_sell_price.setPlaceholderText('Sell price')


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
        self.save_item_push_button.clicked.connect(self.store_data)

        self.grid_layout.addWidget(self.item_name, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.barcode, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.item_type, 2, 0, 1, 2)
        self.grid_layout.addWidget(self.brand, 3, 0, 1, 2)
        self.grid_layout.addWidget(self.supplier, 4, 0, 1, 2)
        self.grid_layout.addWidget(self.sales_group, 5, 0, 1, 2)

        self.grid_layout.addWidget(self.item_cost, 6, 0, 1, 2)
        self.grid_layout.addWidget(self.item_discount, 7, 0, 1, 2)
        self.grid_layout.addWidget(self.item_sell_price, 8, 0, 1, 2)

        self.grid_layout.addWidget(self.expiry_date, 9, 0, 1, 2)
        self.grid_layout.addWidget(self.effective_date, 10, 0, 1, 2)
        self.grid_layout.addWidget(self.track_inventory, 11, 0, 1, 2)
        self.grid_layout.addWidget(self.option_y_radio_button, 12, 0)
        self.grid_layout.addWidget(self.option_n_radio_button, 12, 1)
        self.grid_layout.addWidget(self.on_hand, 13, 0, 1, 2)
        self.grid_layout.addWidget(self.available, 14, 0, 1, 2)
        self.grid_layout.addWidget(self.save_item_push_button, 15, 0, 1, 2)

        self.setLayout(self.grid_layout)

    def inventory_option(self, option):
        if option == 'No':
            self.on_hand.setEnabled(False)
            self.available.setEnabled(False)
        elif option == 'Yes':
            self.on_hand.setEnabled(True)
            self.available.setEnabled(True)

    def store_data(self):
        print("store_data method called")

        item_name = self.item_name.text()
        barcode = self.barcode.text()
        item_type = self.item_type.currentText()
        brand = self.brand.currentText()
        supplier = self.supplier.currentText()
        sales_group = self.sales_group.currentText()
        item_cost = float(self.item_cost.text()) if self.item_cost.text() else 0.0
        item_discount = float(self.item_discount.text()) if self.item_discount.text() else 0.0
        item_sell_price = float(self.item_sell_price.text()) if self.item_sell_price.text() else 0.0
        expiry_date = self.expiry_date.date().toString(Qt.DateFormat.ISODate)
        effective_date = self.effective_date.date().toString(Qt.DateFormat.ISODate)
        
        # You can add the logic to save these values to the database here
        # Example: Call a function to update the database record using these values

        self.salesdb_functions = SalesDBFunctions()

        # Retrieve the IDs using the SalesDBFunctions methods
        item_id = self.salesdb_functions.get_item_id(item_name, barcode, expiry_date)
        item_type_id = self.salesdb_functions.get_item_type_id(item_type)
        brand_id = self.salesdb_functions.get_brand_id(brand)
        supplier_id = self.salesdb_functions.get_supplier_id(supplier)
        sales_group_id = self.salesdb_functions.get_sales_group_id(sales_group)
        item_price_id = self.salesdb_functions.get_item_price_id(item_cost, item_discount, item_sell_price, effective_date)

        self.salesdb_functions.update_item_table(item_name, barcode, expiry_date, item_id)
        self.salesdb_functions.update_item_type_table(item_type, item_type_id)
        self.salesdb_functions.update_item_brand_table(brand, brand_id)
        self.salesdb_functions.update_supplier_table(supplier, supplier_id)
        self.salesdb_functions.update_sales_group_table(sales_group, sales_group_id)
        self.salesdb_functions.update_item_price_table(item_cost, item_discount, item_sell_price, effective_date, item_price_id)
            
        # Emit the signal to indicate that the data has been saved
        self.data_saved.emit()

        # Close the dialog
        self.accept()





if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    sys.exit(pos_app.exec())