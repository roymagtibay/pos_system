import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

# allows importing files from different path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from db_manager.db_manager import CreateDatabaseTable
from db_manager.db_manager import AddData
from db_manager.db_manager import RetrieveData
from db_manager.db_manager import UpdateData

class AddItem(QDialog):
    def __init__(self):
        super().__init__()
        self.create_database_table = CreateDatabaseTable()
        self.add_item_data = AddData()
        self.retrieve_item_id_data = RetrieveData()
        self.update_item_id_data = UpdateData()

        self.setWindowTitle('Add Item')
        self.setGeometry(1000,100,300,300)
        
        self.create_body()
    
    def store_item_data(self, item_name, barcode, expire_dt, item_type, brand, sales_group, supplier, cost, discount, sell_price, effective_dt):
        self.create_database_table.create_database_table()

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

        self.add_item_data.add_item_data(item_name_data, barcode_data, expire_dt_data, item_type_data, brand_data, sales_group_data, supplier_data, cost_data, discount_data, sell_price_data, effective_dt_data)

        self.add_item_data.close()
        
        print('DATA ADDED!')
        
        self.retrieve_item_id(item_name_data, barcode_data, expire_dt_data, item_type_data, brand_data, sales_group_data, supplier_data, cost_data, discount_data, sell_price_data, effective_dt_data)

    def retrieve_item_id(self, item_name, barcode, expire_dt, item_type, brand, sales_group, supplier, cost, discount, sell_price, effective_dt):

        item_type_id_text = self.retrieve_item_id_data.retrieve_item_type_id(item_type)
        brand_id_text = self.retrieve_item_id_data.retrieve_brand_id(brand)
        sales_group_id_text = self.retrieve_item_id_data.retrieve_sales_group_id(sales_group)
        supplier_id_text = self.retrieve_item_id_data.retrieve_supplier_id(supplier)

        item_type_id = int(item_type_id_text)
        brand_id = int(brand_id_text)
        sales_group_id = int(sales_group_id_text)
        supplier_id = int(supplier_id_text)

        item_id_text = self.retrieve_item_id_data.retrieve_item_id(item_name, barcode, expire_dt)
        item_id = int(item_id_text)

        item_price_id_text = self.retrieve_item_id_data.retrieve_item_price_id(cost, discount, sell_price, effective_dt)
        item_price_id = int(item_price_id_text)

        self.retrieve_item_id_data.close()

        os.system('cls')
        # print('RETREIVED >>> item_type_id:', item_type_id)
        # print('RETREIVED >>> brand_id:', brand_id)
        # print('RETREIVED >>> sales_group_id:', sales_group_id)
        # print('RETREIVED >>> supplier_id:', supplier_id)
        # print('RETREIVED >>> item_id:', item_id)
        # print('RETREIVED >>> item_price_id:', item_price_id)

        

        print('ID RETRIEVED!')

        self.update_item_id(item_id, item_price_id, item_type_id, brand_id, sales_group_id, supplier_id, item_name, barcode, expire_dt, cost, discount, sell_price, effective_dt)

    def update_item_id(self, item_id, item_price_id, item_type_id, brand_id, sales_group_id, supplier_id, item_name, barcode, expire_dt, cost, discount, sell_price, effective_dt):
        print('RETREIVED >>> item_type_id:', item_type_id)
        print('RETREIVED >>> brand_id:', brand_id)
        print('RETREIVED >>> sales_group_id:', sales_group_id)
        print('RETREIVED >>> supplier_id:', supplier_id)
        print('RETREIVED >>> item_id:', item_id)
        print('RETREIVED >>> item_price_id:', item_price_id)

        item_type_id_test = int(item_type_id)
        brand_id_test = int(brand_id)
        sales_group_id_test = int(sales_group_id)
        supplier_id_test = int(supplier_id)
        item_id_test = int(item_id)
        item_price_id_test = int(item_price_id)



        self.update_item_id_data.update_table(item_id_test, item_type_id_test, sales_group_id_test, supplier_id_test, item_name, barcode, expire_dt, cost, discount, sell_price, effective_dt)
        print('ID UDPATED!')

        self.update_item_id_data.close()

        self.accept()


    def create_body(self):
        self.body_layout = QGridLayout()

        item_name_field = QComboBox()
        item_name_field.setEditable(True)

        barcode_field = QLineEdit()

        expire_dt_field = QDateEdit()
        expire_dt_field.setDate(QDate.currentDate())

        item_type_field = QComboBox()
        item_type_field.setEditable(True)

        brand_field = QComboBox()
        brand_field.setEditable(True)

        sales_group_field = QComboBox()
        sales_group_field.addItem('Retail')
        sales_group_field.addItem('Wholesale')
        sales_group_field.setEditable(True)

        supplier_field = QComboBox()
        supplier_field.setEditable(True)

        cost_field = QLineEdit()
        discount_field = QLineEdit()
        sell_price_field = QLineEdit()
        effective_dt_field = QDateEdit()
        
        effective_dt_field.setDate(QDate.currentDate())

        save_button = QPushButton('SAVE ITEM')
        save_button.clicked.connect(lambda: self.store_item_data(item_name_field, barcode_field, expire_dt_field, item_type_field, brand_field, sales_group_field, supplier_field, cost_field, discount_field, sell_price_field, effective_dt_field))

        # used for test data
        item_name_field.setCurrentText('Item 1')
        barcode_field.setText('e4isor')
        item_type_field.setCurrentText('Type 1')
        brand_field.setCurrentText('Brand 1')
        supplier_field.setCurrentText('Supplier 1')
        cost_field.setText(str(30.40))
        discount_field.setText(str(10.60))
        sell_price_field.setText(str(50.75))

        self.body_layout.addWidget(item_name_field,0,0)
        self.body_layout.addWidget(barcode_field,1,0)
        self.body_layout.addWidget(expire_dt_field,2,0)
        self.body_layout.addWidget(item_type_field,3,0)
        self.body_layout.addWidget(brand_field,4,0)
        self.body_layout.addWidget(sales_group_field,5,0)
        self.body_layout.addWidget(supplier_field,6,0)
        self.body_layout.addWidget(cost_field,7,0)
        self.body_layout.addWidget(discount_field,8,0)
        self.body_layout.addWidget(sell_price_field,9,0)
        self.body_layout.addWidget(effective_dt_field,10,0)

        self.body_layout.addWidget(save_button,11,0)



        self.setLayout(self.body_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AddItem()
    window.show()
    sys.exit(pos_app.exec())

    