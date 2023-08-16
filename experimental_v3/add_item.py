import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from db_manager import *

class AddItem(QDialog):
    def __init__(self):
        super().__init__()
        self.initiate_query = InitDatabaseTable()
        self.store_query = StoreData()
        self.retrieve_query = RetrieveId()

        self.create_body()
    
    def create_body(self):
        self.initiate_query.database_table()

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

    # widgets attributes
        # for QComboBox (setEditable)
        item_name_field.setEditable(True)
        item_type_field.setEditable(True)
        brand_field.setEditable(True)
        sales_group_field.setEditable(True)
        supplier_field.setEditable(True)

        # for QComboBox (addItem)
        sales_group_field.addItem('Retail')
        sales_group_field.addItem('Wholesale')
        
        # for all widgets (setCurrentText, setText, setDate)
        item_name_field.setCurrentText('Item 1')
        barcode_field.setText('e4isor')
        expire_dt_field.setDate(QDate.currentDate())
        item_type_field.setCurrentText('Type 1')
        brand_field.setCurrentText('Brand 1')
        supplier_field.setCurrentText('Supplier 1')
        cost_field.setText(str(30.40))
        discount_field.setText(str(10.60))
        sell_price_field.setText(str(50.75))
        effective_dt_field.setDate(QDate.currentDate())

        # for QPushButton (clicked.connect)
        save_button.clicked.connect(lambda: self.step_a(item_name_field, barcode_field, expire_dt_field, item_type_field, brand_field, sales_group_field, supplier_field, cost_field, discount_field, sell_price_field, effective_dt_field))

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

    # step_a of add_item (first step)
    def step_a(self, item_name, barcode, expire_dt, item_type, brand, sales_group, supplier, cost, discount, sell_price, effective_dt):
        # store inputs in the variables
        item_name_data = str(item_name.currentText() )
        barcode_data = str(barcode.text())
        expire_dt_data = expire_dt.date().toString(Qt.DateFormat.ISODate)
        item_type_data = str(item_type.currentText())
        brand_data = str(brand.currentText())
        sales_group_data = str(sales_group.currentText())
        supplier_data = str(supplier.currentText())
        cost_data = '{:.2f}'.format(float(cost.text())) 
        discount_data = '{:.2f}'.format(float(discount.text())) 
        sell_price_data = '{:.2f}'.format(float(sell_price.text())) 
        effective_dt_data = effective_dt.date().toString(Qt.DateFormat.ISODate)

        # store variables' values in item_type, brand, sales_group, and supplier table
        self.store_query.item_type_data(item_type_data)
        self.store_query.brand_data(brand_data)
        self.store_query.sales_group_data(sales_group_data)
        self.store_query.supplier_data(supplier_data)

        print(item_name_data, end='')
        print(barcode_data, end='')
        print(expire_dt_data, end='')
        print(item_type_data, end='')
        print(brand_data, end='')
        print(sales_group_data, end='')
        print(supplier_data, end='')
        print(cost_data, end='')
        print(discount_data, end='')
        print(sell_price_data, end='')
        print(effective_dt_data)

        print('step a done!')
        # proceed to step_b (pass the values to step_b parameters)
        self.step_b(item_name_data, barcode_data, expire_dt_data, item_type_data, brand_data, sales_group_data, supplier_data, cost_data, discount_data, sell_price_data, effective_dt_data)

    # step_b of add_item (second step)
    def step_b(self, item_name, barcode, expire_dt, item_type, brand, sales_group, supplier, cost, discount, sell_price, effective_dt):
        # retrieve ids from item_type, brand, sales_group, and supplier table
        item_type_id_text = self.retrieve_query.item_type_id(item_type)
        brand_id_text = self.retrieve_query.brand_id(brand)
        sales_group_id_text = self.retrieve_query.sales_group_id(sales_group)
        supplier_id_text = self.retrieve_query.supplier_id(supplier)

        # convert the retrieve ids into integer and store to the variables
        item_type_id_data = str(item_type_id_text)
        brand_id_data = str(brand_id_text)
        sales_group_id_data = str(sales_group_id_text)
        supplier_id_data = str(supplier_id_text)

        print('step b done!')

        
        # store item data into Item table
        self.store_query.item_data(item_name, barcode, expire_dt, item_type_id_data, brand_id_data, sales_group_id_data, supplier_id_data)

        # retrieve id from item
        item_id_text = self.retrieve_query.item_id(item_name, barcode, expire_dt, item_type_id_data, brand_id_data, sales_group_id_data, supplier_id_data)

        # convert the retrieve id into integer and store to the variables
        item_id_data = int(item_id_text)

        print(item_id_text, end=', ')
        print(item_type_id_text, end=', ')
        print(brand_id_text, end='')
        print(sales_group_id_text, end=', ')
        print(supplier_id_text, end=', ')

        # proceed to step_c (pass the values to step_c parameters)
        self.step_c(item_id_data, cost, discount, sell_price, effective_dt)

    # step_c of add_item (third step)
    def step_c(self, item_id_data, cost, discount, sell_price, effective_dt):
        print('step c done!')
        
        # store item_price data into ItemPrice table
        self.store_query.item_price_data(item_id_data, cost, discount, sell_price, effective_dt)

        print(item_id_data, end=', ')
        print(cost, end=', ')
        print(discount, end=', ')
        print(sell_price, end=', ')
        print(effective_dt, end=', ')
        

        
        
        
        

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddItem()
    window.show()
    sys.exit(pos_app.exec())