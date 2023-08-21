import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.item_management_sql import *

class ItemManagementWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_layout()

    # call 'AddItemDialog(QDialog)'
    def open_add_item_window(self):
        add_item_dialog = AddItemDialog()
        add_item_dialog.data_saved.connect(lambda: self.list_item_table.display_item_table(''))
        add_item_dialog.exec()
    
    # filter item flag
    def filter_item(self):
        filter_input = self.filter_item_field.text()

        if filter_input == '':
            self.list_item_table.display_item_table(filter_input)
        else:
            self.list_item_table.filter_item_table(filter_input)

    def init_layout(self):
        self.layout = QGridLayout()

        self.filter_item_field = QLineEdit()
        self.filter_item_field.setPlaceholderText('Filter item by item name, barcode, item type, etc...')
        add_item_button = QPushButton('ADD')

        self.list_item_table = ListItemTable() # -- class ListItemTable(QTableWidget)

        self.filter_item_field.textChanged.connect(self.filter_item) # connects to filter_item functions every change of text
        add_item_button.clicked.connect(self.open_add_item_window) # connects to open_add_item_window every click of button

        self.layout.addWidget(self.filter_item_field,0,0)
        self.layout.addWidget(add_item_button,0,1)
        self.layout.addWidget(self.list_item_table,1,0,1,2)

        self.setLayout(self.layout)

class AddItemDialog(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.call_sql_utils()
        self.init_layout()
    
    # call sql queries 
    def call_sql_utils(self):
        self.create_table = CreateDatabaseTable()
        self.insert_data = InsertItemData()
        self.select_id = SelectItemId()
        self.select_data = SelectItemData()

    # fills the 'QComboBoxes' with registered data in SALES.db
    def fill_combobox(self):
        items = self.select_data.items()
        for row in items:
            self.item_name.addItem(row)

        item_types = self.select_data.item_types()
        for row in item_types:
            self.item_type.addItem(row)

        brands = self.select_data.brands()
        for row in brands:
            self.brand.addItem(row)

        sales_groups = self.select_data.sales_groups()
        for row in sales_groups:
            self.sales_group.addItem(row)

        suppliers = self.select_data.suppliers()
        for row in suppliers:
            self.supplier.addItem(row)

    # main layout of class AddItemDialog(QDialog)
    def init_layout(self):
        self.layout = QGridLayout()


        self.item_name = QComboBox()
        self.item_name.setEditable(True)
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText('Barcode')
        self.expire_dt = QDateEdit()
        self.expire_dt.setDate(QDate.currentDate())
        self.item_type = QComboBox()
        self.item_type.setEditable(True)
        self.brand = QComboBox()
        self.brand.setEditable(True)
        self.sales_group = QComboBox()
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')
        self.supplier = QComboBox()
        self.supplier.setEditable(True)
        self.cost = QLineEdit()
        self.cost.setPlaceholderText('Cost')
        self.discount = QLineEdit()
        self.discount.setPlaceholderText('Discount')
        self.sell_price = QLineEdit()
        self.sell_price.setPlaceholderText('Sell price')
        self.effective_dt = QDateEdit()
        self.effective_dt.setDate(QDate.currentDate())
        self.track_inventory_label = QLabel('Track inventory for this item?')
        self.track_inventory_y = QRadioButton('Yes')
        self.track_inventory_n = QRadioButton('No')
        self.on_hand_stock = QLineEdit()
        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.available_stock = QLineEdit()
        self.available_stock.setPlaceholderText('Available stock')
        self.save_button = QPushButton('SAVE')

        self.item_name.setCurrentText('Item 1')
        self.barcode.setText('e4isor')
        self.expire_dt.setDate(QDate.currentDate())
        self.item_type.setCurrentText('Type 1')
        self.brand.setCurrentText('Brand 1')
        self.supplier.setCurrentText('Supplier 1')
        self.cost.setText(str(30.40))
        self.discount.setText(str(10.60))
        self.sell_price.setText(str(50.75))
        self.effective_dt.setDate(QDate.currentDate())

        self.fill_combobox()
        self.save_button.clicked.connect(lambda: self.step_a(self.item_type, self.brand, self.sales_group, self.supplier, self.item_name, self.barcode, self.expire_dt, self.cost, self.discount, self.sell_price, self.effective_dt))

        self.layout.addWidget(self.item_name)
        self.layout.addWidget(self.barcode)
        self.layout.addWidget(self.expire_dt)
        self.layout.addWidget(self.item_type)
        self.layout.addWidget(self.brand)
        self.layout.addWidget(self.sales_group)
        self.layout.addWidget(self.supplier)
        self.layout.addWidget(self.cost)
        self.layout.addWidget(self.discount)
        self.layout.addWidget(self.sell_price)
        self.layout.addWidget(self.effective_dt)
        self.layout.addWidget(self.track_inventory_label)
        self.layout.addWidget(self.track_inventory_y)
        self.layout.addWidget(self.track_inventory_n)
        self.layout.addWidget(self.on_hand_stock)
        self.layout.addWidget(self.available_stock)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    # functions labeled as steps for adding items
    # init data base table and convert raw values
    def step_a(self, raw_item_type, raw_brand, raw_sales_group, raw_supplier, raw_item_name, raw_barcode, raw_expire_dt, raw_cost, raw_discount, raw_sell_price, raw_effective_dt): 
        self.create_table.database_table()
        
        # ItemType, Brand, SalesGroup, and Supplier table
        converted_item_type = str(raw_item_type.currentText())
        converted_brand = str(raw_brand.currentText())
        converted_sales_group = str(raw_sales_group.currentText())
        converted_supplier = str(raw_supplier.currentText())

        # Item table
        converted_item_name = str(raw_item_name.currentText())
        converted_barcode = str(raw_barcode.text())
        converted_expire_dt = raw_expire_dt.date().toString(Qt.DateFormat.ISODate)

        # ItemPrice table
        converted_cost = '{:.2f}'.format(float(raw_cost.text()))
        converted_discount = '{:.2f}'.format(float(raw_discount.text()))
        converted_sell_price = '{:.2f}'.format(float(raw_sell_price.text()))
        converted_effective_dt = raw_effective_dt.date().toString(Qt.DateFormat.ISODate)
        
        print('add_item: step_a -- done')

        # pass values to step_b parameters
        self.step_b(converted_item_type, converted_brand, converted_sales_group, converted_supplier, converted_item_name, converted_barcode, converted_expire_dt, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)
        
    # store item_type, brand, sales_group, and supplier data
    def step_b(self, converted_item_type, converted_brand, converted_sales_group, converted_supplier, converted_item_name, converted_barcode, converted_expire_dt, converted_cost, converted_discount, converted_sell_price, converted_effective_dt): 
        self.insert_data.item_type_data(converted_item_type)
        self.insert_data.brand_data(converted_brand)
        self.insert_data.sales_group_data(converted_sales_group)
        self.insert_data.supplier_data(converted_supplier)

        print('add_item: step_b -- done')

        self.step_c(converted_item_type, converted_brand, converted_sales_group, converted_supplier, converted_item_name, converted_barcode, converted_expire_dt, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)

    # retrieve item_type, brand, sales_group, and supplier ids and store item data (item_name, barcode, expire_dt)
    def step_c(self, converted_item_type, converted_brand, converted_sales_group, converted_supplier, converted_item_name, converted_barcode, converted_expire_dt, converted_cost, converted_discount, converted_sell_price, converted_effective_dt): 
        converted_item_type_id = int(self.select_id.item_type_id(converted_item_type))
        converted_brand_id = int(self.select_id.brand_id(converted_brand))
        converted_sales_group_id = int(self.select_id.sales_group_id(converted_sales_group))
        converted_supplier_id = int(self.select_id.supplier_id(converted_supplier))

        self.insert_data.item_data(converted_item_name, converted_barcode, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

        print('add_item: step_c -- done')

        self.step_d(converted_item_name, converted_barcode, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)

    # store item (item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, and supplier_id) and item_price data (item_id, cost, discount, sell_price, and effective_dt)
    def step_d(self, converted_item_name, converted_barcode, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt): 
        converted_item_id = int(self.select_id.item_id(converted_item_name, converted_barcode, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id))

        self.insert_data.item_price_data(converted_item_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)

        print('add_item: step_d -- done')

        self.data_saved.emit()

        self.accept()

class EditItemDialog(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.call_sql_utils()
        self.init_layout(row_index, row_value)
    
    # call sql queries 
    def call_sql_utils(self):
        self.create_table = CreateDatabaseTable()
        self.update_data = UpdateItemData()
        self.select_id = SelectItemId()

    # main layout of 'EditItemDialog(QDialog)'
    def init_layout(self, row_index, row_value):
        self.layout = QGridLayout()

        item_name = QComboBox()
        item_name.setEditable(True)
        barcode = QLineEdit()
        barcode.setPlaceholderText('Barcode')
        expire_dt = QDateEdit()
        expire_dt.setDate(QDate.currentDate())
        item_type = QComboBox()
        item_type.setDisabled(True)
        item_type.setEditable(True)
        brand = QComboBox()
        brand.setDisabled(True)
        brand.setEditable(True)
        sales_group = QComboBox()
        sales_group.setDisabled(True)
        sales_group.addItem('Retail')
        sales_group.addItem('Wholesale')
        supplier = QComboBox()
        supplier.setDisabled(True)
        supplier.setEditable(True)
        cost = QLineEdit()
        cost.setDisabled(True)
        cost.setPlaceholderText('Cost')
        discount = QLineEdit()
        discount.setDisabled(True)
        discount.setPlaceholderText('Discount')
        sell_price = QLineEdit()
        sell_price.setDisabled(True)
        sell_price.setPlaceholderText('Sell price')
        effective_dt = QDateEdit()
        effective_dt.setDisabled(True)
        effective_dt.setDate(QDate.currentDate())
        save_button = QPushButton('SAVE')

        item_name.setCurrentText(row_value[0])
        barcode.setText(row_value[1])
        expire_dt.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))
        item_type.setCurrentText(row_value[3])
        brand.setCurrentText(row_value[4])
        sales_group.setCurrentText(row_value[5])
        supplier.setCurrentText(row_value[6])
        cost.setText(str(row_value[7]))
        discount.setText(str(row_value[8]))
        sell_price.setText(str(row_value[9]))
        effective_dt.setDate(QDate.fromString(row_value[10], Qt.DateFormat.ISODate))

        save_button.clicked.connect(lambda: self.step_a(item_name, barcode, expire_dt, row_value))

        self.layout.addWidget(item_name)
        self.layout.addWidget(barcode)
        self.layout.addWidget(expire_dt)
        self.layout.addWidget(item_type)
        self.layout.addWidget(brand)
        self.layout.addWidget(sales_group)
        self.layout.addWidget(supplier)
        self.layout.addWidget(cost)
        self.layout.addWidget(discount)
        self.layout.addWidget(sell_price)
        self.layout.addWidget(effective_dt)
        self.layout.addWidget(save_button)

        self.setLayout(self.layout)

    # functions labeled as steps for editing items
    def step_a(self, raw_item_name, raw_barcode, raw_expire_dt, row_value):
        # Item table data
        converted_item_name = str(raw_item_name.currentText())
        converted_barcode = str(raw_barcode.text())
        converted_expire_dt = raw_expire_dt.date().toString(Qt.DateFormat.ISODate)

        # ItemType, Brand, SalesGroup, and Supplier table id
        converted_item_id = int(row_value[11])
        converted_item_type_id = int(row_value[12])
        converted_brand_id = int(row_value[13])
        converted_sales_group_id = int(row_value[14])
        converted_supplier_id = int(row_value[15])

        # update item table data
        self.update_data.item_data(converted_item_name, converted_barcode, converted_expire_dt, converted_item_id, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

        self.data_saved.emit()

        self.accept()

class ListItemTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.call_sql_utils()
        self.init_layout()

    # call sql queries 
    def call_sql_utils(self):
        self.select_data = SelectItemData()

    # call 'EditItemDialog(QDialog)'
    def open_edit_item_window(self, row_index, row_value):
        edit_item_dialog = EditItemDialog(row_index, row_value)
        edit_item_dialog.data_saved.connect(lambda: self.display_item_table(''))
        edit_item_dialog.exec()

    # displays filtered items
    def filter_item_table(self, filter_text):
        filtered_item_data = self.select_data.filtered_item_data(filter_text)

        self.setRowCount(len(filtered_item_data))
        
        for row_index, row_value in enumerate(filtered_item_data):
            row_cell_limit = row_value[:11] # limits the data shown in the table

            for col_index, col_value in enumerate(row_cell_limit):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))

            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.open_edit_item_window(row_index, row_value))
            self.setCellWidget(row_index, 0, self.edit_tem_button)

    # displays 50 recently added items
    def display_item_table(self, text):
        all_item_data = self.select_data.all_item_data(text)

        self.setRowCount(50)
        
        for row_index, row_value in enumerate(all_item_data):
            row_cell_limit = row_value[:11] # limits the data shown in the table

            for col_index, col_value in enumerate(row_cell_limit):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))

            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.open_edit_item_window(row_index, row_value))
            self.setCellWidget(row_index, 0, self.edit_tem_button)

    # main layout of 'ListItemTable(QTableWidget)'
    def init_layout(self):
        
        self.setColumnCount(12)
        self.setHorizontalHeaderLabels(['','Item name','Barcode','Expire date','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Effective date'])
        
        # sets the value of the parameter of display_item_table function to ''
        self.display_item_table('')
        
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagementWidget()
    window.show()
    sys.exit(pos_app.exec())
