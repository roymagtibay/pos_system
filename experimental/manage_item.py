import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from database_manager import EditItemQuery
from database_manager import AddItemQuery

class EditItem(QDialog):
    data_stored = pyqtSignal()

    def __init__(self, row, item):
        super().__init__()

        self.setWindowTitle('Edit item')

        self.edit_item_query = EditItemQuery()

        self.create_body(item) # allows the user of widgets in different functions
    
    def create_body(self, item):
        self.layout = QGridLayout()



        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText('Item name')
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText('Barcode')
        self.expire_date = QDateEdit()

        self.item_type = QComboBox()
        self.item_type.setPlaceholderText('Item type')
        self.item_type.setEditable(True)
        self.brand_name = QComboBox()
        self.brand_name.setPlaceholderText('Brand name')
        self.brand_name.setEditable(True)
        
        self.sales_group_name = QComboBox()
        self.sales_group_name.addItem('Retail')
        self.sales_group_name.addItem('Wholesale')

        self.supplier_name = QComboBox()
        self.supplier_name.setPlaceholderText('Supplier')
        self.supplier_name.setEditable(True)

        self.cost = QLineEdit()
        self.cost.setPlaceholderText('Cost')
        self.discount = QLineEdit()
        self.discount.setPlaceholderText('Discount')
        self.sell_price = QLineEdit()
        self.sell_price.setPlaceholderText('Sell price')
        self.effective_date = QDateEdit()

        self.save_button = QPushButton('SAVE ITEM')
        self.save_button.clicked.connect(lambda: self.store_data(self.item_name, self.barcode, self.expire_date, self.item_type, self.brand_name, self.sales_group_name, self.supplier_name, self.cost, self.discount, self.sell_price, self.effective_date))

        self.item_name.setText(item[0])
        self.barcode.setText(item[1])
        self.expire_date.setDate(QDate.fromString(item[2], Qt.DateFormat.ISODate))
        self.item_type.setCurrentText(item[3])
        self.brand_name.setCurrentText(item[4])
        self.sales_group_name.setCurrentText(item[5])
        self.supplier_name.setCurrentText(item[6])
        self.cost.setText(str(item[7]))
        self.discount.setText(str(item[8]))
        self.sell_price.setText(str(item[9]))
        self.effective_date.setDate(QDate.fromString(item[10], Qt.DateFormat.ISODate))





        self.layout.addWidget(self.item_name)
        self.layout.addWidget(self.barcode)
        self.layout.addWidget(self.expire_date)
        self.layout.addWidget(self.item_type)
        self.layout.addWidget(self.brand_name)
        self.layout.addWidget(self.sales_group_name)
        self.layout.addWidget(self.supplier_name)
        self.layout.addWidget(self.cost)
        self.layout.addWidget(self.discount)
        self.layout.addWidget(self.sell_price)
        self.layout.addWidget(self.effective_date)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def store_data(self, item_name_data, barcode_data, expire_date_data, item_type_data, brand_name_data, sales_group_name_data, supplier_name_data, cost_data, discount_data, sell_price_data, effective_date_data):

        item_name_data = self.item_name.text()
        barcode_data = self.barcode.text()
        expire_date_data = self.expire_date.date().toString(Qt.DateFormat.ISODate)

        item_type_data = self.item_type.currentText()
        brand_name_data = self.brand_name.currentText()
        sales_group_name_data = self.sales_group_name.currentText()
        supplier_name_data = self.supplier_name.currentText()

        cost_data_text = self.cost.text()
        discount_data_text = self.discount.text()
        sell_price_data_text = self.sell_price.text()

        cost_data = float(cost_data_text) if cost_data_text else 0.00
        discount_data = float(discount_data_text) if discount_data_text else 0.00
        sell_price_data = float(sell_price_data_text) if sell_price_data_text else 0.00

        effective_date_data = self.effective_date.date().toString(Qt.DateFormat.ISODate)

        self.item_id = self.edit_item_query.retrieve_item_id(item_name_data)
        
        self.edit_item_query.change_item_data(item_name_data, barcode_data, expire_date_data, self.item_id)

        # self.edit_item_query.change_item_type_data(item_type_data, self.item_id)
        # self.edit_item_query.change_brand_data(brand_name_data, self.item_id)
        # self.edit_item_query.change_sales_group_data(sales_group_name_data, self.item_id)
        # self.edit_item_query.change_supplier_data(supplier_name_data, self.item_id)
        # self.edit_item_query.change_item_price_data(cost_data, discount_data, sell_price_data, effective_date_data, self.item_id)

        self.data_stored.emit()

        self.edit_item_query.close()
    
        self.accept()

class AddItem(QDialog):
    data_stored = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add item')

        self.add_item_query = AddItemQuery()

        self.create_body() # allows the user of widgets in different functions

    # Stores data to the 'SALES.db'
    def store_data(self, item_name_data, barcode_data, expire_date_data, item_type_data, brand_name_data, sales_group_name_data, supplier_name_data, cost_data, discount_data, sell_price_data, effective_date_data): # 
        
        item_name_data = self.item_name.text()
        barcode_data = self.barcode.text()
        expire_date_data = self.expire_date.date().toString(Qt.DateFormat.ISODate)

        item_type_data = self.item_type.currentText()
        brand_name_data = self.brand_name.currentText()
        sales_group_name_data = self.sales_group_name.currentText()
        supplier_name_data = self.supplier_name.currentText()

        cost_data_text = self.cost.text()
        discount_data_text = self.discount.text()
        sell_price_data_text = self.sell_price.text()

        cost_data = float(cost_data_text) if cost_data_text else 0.00
        discount_data = float(discount_data_text) if discount_data_text else 0.00
        sell_price_data = float(sell_price_data_text) if sell_price_data_text else 0.00

        effective_date_data = self.effective_date.date().toString(Qt.DateFormat.ISODate)

        self.add_item_query.store_item_data(item_name_data, barcode_data, expire_date_data)
        self.add_item_query.store_item_type_data(item_type_data)
        self.add_item_query.store_brand_data(brand_name_data)
        self.add_item_query.store_sales_group_data(sales_group_name_data)
        self.add_item_query.store_supplier_data(supplier_name_data)
        self.add_item_query.store_item_price_data(cost_data, discount_data, sell_price_data, effective_date_data)

        self.retrieve_id(item_name_data, item_type_data, brand_name_data, sales_group_name_data, supplier_name_data, cost_data, discount_data, sell_price_data)


    def retrieve_id(self, item_name_data, item_type_data, brand_name_data, sales_group_name_data, supplier_name_data, cost_data, discount_data, sell_price_data):
        
        item_name_data = self.item_name.text()

        item_type_data = self.item_type.currentText()
        brand_name_data = self.brand_name.currentText()
        sales_group_name_data = self.sales_group_name.currentText()
        supplier_name_data = self.supplier_name.currentText()

        cost_data_text = self.cost.text()
        discount_data_text = self.discount.text()
        sell_price_data_text = self.sell_price.text()

        cost_data = float(cost_data_text) if cost_data_text else 0.00
        discount_data = float(discount_data_text) if discount_data_text else 0.00
        sell_price_data = float(sell_price_data_text) if sell_price_data_text else 0.00

        # retrieve ids from 'SALES.db'
        item_id_text = self.add_item_query.retrieve_item_id(item_name_data)
        item_type_id_text = self.add_item_query.retrieve_item_type_id(item_type_data)
        brand_id_text = self.add_item_query.retrieve_brand_id(brand_name_data)
        sales_group_id_text = self.add_item_query.retrieve_sales_group_id(sales_group_name_data)
        supplier_id_text = self.add_item_query.retrieve_supplier_id(supplier_name_data)
        item_price_id_text = self.add_item_query.retrieve_item_price_id(cost_data, discount_data, sell_price_data)


        # conversion
        item_id = int(item_id_text) if item_id_text else None
        item_type_id = int(item_type_id_text) if item_type_id_text else None
        brand_id = int(brand_id_text) if brand_id_text else None
        sales_group_id = int(sales_group_id_text) if sales_group_id_text else None
        supplier_id = int(supplier_id_text) if supplier_id_text else None
        item_price_id = int(item_price_id_text) if item_price_id_text else None
        
        self.store_id(item_name_data, item_id, item_type_id, brand_id, sales_group_id, supplier_id, item_price_id)

        os.system('cls')
        print('This is the item_id:', item_id)
        print('This is the item_type_id:', item_type_id)
        print('This is the brand_id:', brand_id)
        print('This is the sales_group_id:', sales_group_id)
        print('This is the supplier_id:', supplier_id)
        print('This is the item_price_id:', item_price_id)


    def store_id(self, item_name_data, item_id, item_type_id, brand_id, sales_group_id, supplier_id, item_price_id):
        self.add_item_query = AddItemQuery()

        self.add_item_query.store_id_to_item(item_type_id,  brand_id, sales_group_id, supplier_id, item_name_data)
        self.add_item_query.store_id_to_item_price_data(item_id, item_price_id)

        self.data_stored.emit()

        self.add_item_query.close()
    
        self.accept()


        

    def create_body(self):
        self.layout = QGridLayout()

        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText('Item name')
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText('Barcode')
        self.expire_date = QDateEdit()
        self.expire_date.setDate(QDate.currentDate())

        self.item_type = QComboBox()
        self.item_type.setPlaceholderText('Item type')
        self.item_type.setEditable(True)
        self.brand_name = QComboBox()
        self.brand_name.setPlaceholderText('Brand name')
        self.brand_name.setEditable(True)
        
        self.sales_group_name = QComboBox()
        self.sales_group_name.addItem('Retail')
        self.sales_group_name.addItem('Wholesale')

        self.supplier_name = QComboBox()
        self.supplier_name.setPlaceholderText('Supplier')
        self.supplier_name.setEditable(True)

        self.cost = QLineEdit()
        self.cost.setPlaceholderText('Cost')
        self.discount = QLineEdit()
        self.discount.setPlaceholderText('Discount')
        self.sell_price = QLineEdit()
        self.sell_price.setPlaceholderText('Sell price')
        self.effective_date = QDateEdit()
        self.effective_date.setDate(QDate.currentDate())

        self.save_button = QPushButton('SAVE ITEM')
        self.save_button.clicked.connect(lambda: self.store_data(self.item_name, self.barcode, self.expire_date, self.item_type, self.brand_name, self.sales_group_name, self.supplier_name, self.cost, self.discount, self.sell_price, self.effective_date))

        self.layout.addWidget(self.item_name)
        self.layout.addWidget(self.barcode)
        self.layout.addWidget(self.expire_date)
        self.layout.addWidget(self.item_type)
        self.layout.addWidget(self.brand_name)
        self.layout.addWidget(self.sales_group_name)
        self.layout.addWidget(self.supplier_name)
        self.layout.addWidget(self.cost)
        self.layout.addWidget(self.discount)
        self.layout.addWidget(self.sell_price)
        self.layout.addWidget(self.effective_date)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

