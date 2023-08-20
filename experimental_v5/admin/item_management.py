import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_manager import *

class EditItemWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.change_query = ChangeData()

        self.create_layout(row_index, row_value)

    def step_a(self, raw_item_name, raw_barcode, raw_expire_dt, converted_item_id, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id):
        converted_item_name = str(raw_item_name.currentText())
        converted_barcode = str(raw_barcode.text())
        converted_expire_dt = raw_expire_dt.date().toString(Qt.DateFormat.ISODate)

        self.change_query.all_item_data(converted_item_name, converted_barcode, converted_expire_dt, converted_item_id, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

        self.data_saved.emit()

        self.accept()

    def create_layout(self, row_index, row_value):
        self.layout = QGridLayout()

        self.disable_item = QLabel('Disable this item?')
        self.disable_item_y = QRadioButton('Yes')
        self.disable_item_n = QRadioButton('No')
        self.item_name_field = QComboBox()
        self.barcode_field = QLineEdit()
        self.expire_dt_field = QDateEdit()
        self.item_type_field = QComboBox()
        self.brand_field = QComboBox()
        self.sales_group_field = QComboBox()
        self.supplier_field = QComboBox()
        self.cost_field = QLineEdit()
        self.discount_field = QLineEdit()
        self.sell_price_field = QLineEdit()
        self.effective_dt_field = QDateEdit()
        self.save_item_button = QPushButton('SAVE ITEM')

        self.disable_item_n.setChecked(True)
        self.item_name_field.setEditable(True)
        self.barcode_field.setPlaceholderText('Barcode')
        self.expire_dt_field.setDate(QDate.currentDate())
        self.item_type_field.setEditable(True)
        self.brand_field.setEditable(True)
        self.sales_group_field.addItem('Retail')
        self.sales_group_field.addItem('Wholesale')
        self.supplier_field.setEditable(True)

        self.item_type_field.setDisabled(True)
        self.brand_field.setDisabled(True)
        self.sales_group_field.setDisabled(True)
        self.supplier_field.setDisabled(True)
        self.cost_field.setDisabled(True)
        self.discount_field.setDisabled(True)
        self.sell_price_field.setDisabled(True)
        self.effective_dt_field.setDisabled(True)

        self.cost_field.setDisabled(True)
        self.discount_field.setDisabled(True)
        self.sell_price_field.setDisabled(True)
        self.effective_dt_field.setDisabled(True)

    # store data to row_value[]
        self.item_name_field.setCurrentText(row_value[0])
        self.barcode_field.setText(row_value[1])
        self.expire_dt_field.setDate(QDate.fromString(row_value[2], Qt.DateFormat.ISODate))
        self.item_type_field.setCurrentText(row_value[3])
        self.brand_field.setCurrentText(row_value[4])
        self.sales_group_field.setCurrentText(row_value[5])
        self.supplier_field.setCurrentText(row_value[6])
        self.cost_field.setText(str(row_value[7]))
        self.discount_field.setText(str(row_value[8]))
        self.sell_price_field.setText(str(row_value[9]))
        self.effective_dt_field.setDate(QDate.fromString(row_value[10], Qt.DateFormat.ISODate))

        self.item_id_data = int(row_value[11])
        self.item_type_id_data = int(row_value[12])
        self.brand_id_data = int(row_value[13])
        self.sales_group_id_data = int(row_value[14])
        self.supplier_id_data = int(row_value[15])

        print('IDs:')
        print(self.item_id_data, end=', ')
        print(self.item_type_id_data, end=', ')
        print(self.brand_id_data, end=', ')
        print(self.sales_group_id_data, end=', ')
        print(self.supplier_id_data, end=', ')

        self.save_item_button.clicked.connect(lambda: self.step_a(self.item_name_field, self.barcode_field, self.expire_dt_field, self.item_id_data, self.item_type_id_data, self.brand_id_data, self.sales_group_id_data, self.supplier_id_data))

        self.layout.addWidget(self.disable_item)
        self.layout.addWidget(self.disable_item_y)
        self.layout.addWidget(self.disable_item_n)
        self.layout.addWidget(self.item_name_field)
        self.layout.addWidget(self.barcode_field)
        self.layout.addWidget(self.expire_dt_field)
        self.layout.addWidget(self.item_type_field)
        self.layout.addWidget(self.brand_field)
        self.layout.addWidget(self.sales_group_field)
        self.layout.addWidget(self.supplier_field)
        self.layout.addWidget(self.cost_field)
        self.layout.addWidget(self.discount_field)
        self.layout.addWidget(self.sell_price_field)
        self.layout.addWidget(self.effective_dt_field)
        self.layout.addWidget(self.save_item_button)

        self.setLayout(self.layout)

class AddItemWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')

        self.store_query = StoreData()
        self.retrieve_data_id = RetrieveId()

        self.create_layout()

    def display_inventory_field(self, flag):
        if flag == 'Yes':
            self.on_hand_stock_field.show()
            self.available_stock_field.show()

        elif flag == 'No':
            self.on_hand_stock_field.hide()
            self.available_stock_field.hide()

    def step_a(self, raw_item_name, raw_barcode, raw_expire_dt, raw_item_type, raw_brand, raw_sales_group, raw_supplier, raw_cost, raw_discount, raw_sell_price, raw_effective_dt):
        converted_item_type = str(raw_item_type.currentText())
        converted_brand = str(raw_brand.currentText())
        converted_sales_group = str(raw_sales_group.currentText())
        converted_supplier = str(raw_supplier.currentText())

        self.store_query.item_type_data(converted_item_type)
        self.store_query.brand_data(converted_brand)
        self.store_query.sales_group_data(converted_sales_group)
        self.store_query.supplier_data(converted_supplier)

        print('step a done!')
        self.step_b(raw_item_name, raw_barcode, raw_expire_dt, converted_item_type, converted_brand, converted_sales_group, converted_supplier, raw_cost, raw_discount, raw_sell_price, raw_effective_dt)

    def step_b(self, raw_item_name, raw_barcode, raw_expire_dt, converted_item_type, converted_brand, converted_sales_group, converted_supplier, raw_cost, raw_discount, raw_sell_price, raw_effective_dt):
        converted_item_name = str(raw_item_name.currentText())
        converted_barcode = str(raw_barcode.text())
        converted_expire_dt = raw_expire_dt.date().toString(Qt.DateFormat.ISODate)

        retrieved_item_type_id = int(self.retrieve_data_id.item_type_id(converted_item_type))
        retrieved_brand_id = int(self.retrieve_data_id.brand_id(converted_brand))
        retrieved_sales_group_id = int(self.retrieve_data_id.sales_group_id(converted_sales_group))
        retrieved_supplier_id = int(self.retrieve_data_id.supplier_id(converted_supplier))

        print('step b done!')

        self.store_query.item_data(converted_item_name, converted_barcode, converted_expire_dt, retrieved_item_type_id, retrieved_brand_id, retrieved_sales_group_id, retrieved_supplier_id)

        self.step_c(converted_item_name, converted_barcode, converted_expire_dt, retrieved_item_type_id, retrieved_brand_id, retrieved_sales_group_id, retrieved_supplier_id, raw_cost, raw_discount, raw_sell_price, raw_effective_dt)

    def step_c(self, converted_item_name, converted_barcode, converted_expire_dt, retrieved_item_type_id, retrieved_brand_id, retrieved_sales_group_id, retrieved_supplier_id, raw_cost, raw_discount, raw_sell_price, raw_effective_dt):
        converted_cost = '{:.2f}'.format(float(raw_cost.text())) 
        converted_discount = '{:.2f}'.format(float(raw_discount.text())) 
        converted_sell_price = '{:.2f}'.format(float(raw_sell_price.text())) 
        converted_effective_dt = raw_effective_dt.date().toString(Qt.DateFormat.ISODate)

        retrieved_item_id = int(self.retrieve_data_id.item_id(converted_item_name, converted_barcode, converted_expire_dt, retrieved_item_type_id, retrieved_brand_id, retrieved_sales_group_id, retrieved_supplier_id))

        print('step c done!')

        self.store_query.item_price_data(retrieved_item_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)
        
        self.data_saved.emit()

        self.accept()
        
    def create_layout(self):
        self.layout = QGridLayout()

        self.item_name_field = QComboBox()
        self.barcode_field = QLineEdit()
        self.expire_dt_field = QDateEdit()
        self.item_type_field = QComboBox()
        self.brand_field = QComboBox()
        self.sales_group_field = QComboBox()
        self.supplier_field = QComboBox()
        self.cost_field = QLineEdit()
        self.discount_field = QLineEdit()
        self.sell_price_field = QLineEdit()
        self.effective_dt_field = QDateEdit()
        self.track_inventory = QLabel('Track inventory for this item?')
        self.track_inventory_y = QRadioButton('Yes')
        self.track_inventory_n = QRadioButton('No')
        self.on_hand_stock_field = QLineEdit()
        self.available_stock_field = QLineEdit()
        self.spacer = QFrame()
        self.save_item_button = QPushButton('SAVE ITEM')

        self.item_name_field.setEditable(True)
        self.barcode_field.setPlaceholderText('Barcode')
        self.expire_dt_field.setDate(QDate.currentDate())
        self.item_type_field.setEditable(True)
        self.brand_field.setEditable(True)
        self.sales_group_field.addItem('Retail')
        self.sales_group_field.addItem('Wholesale')
        self.supplier_field.setEditable(True)
        self.cost_field.setPlaceholderText('Cost')
        self.track_inventory_y.setChecked(True)
        self.discount_field.setPlaceholderText('Discount')
        self.sell_price_field.setPlaceholderText('Sell price')
        self.effective_dt_field.setDate(QDate.currentDate())

         # !!! sample data for testing !!!
        self.item_name_field.setCurrentText('Item 1')
        self.barcode_field.setText('e4isor')
        self.expire_dt_field.setDate(QDate.currentDate())
        self.item_type_field.setCurrentText('Type 1')
        self.brand_field.setCurrentText('Brand 1')
        self.supplier_field.setCurrentText('Supplier 1')
        self.cost_field.setText(str(30.40))
        self.discount_field.setText(str(10.60))
        self.sell_price_field.setText(str(50.75))
        self.effective_dt_field.setDate(QDate.currentDate())

        self.track_inventory_y.clicked.connect(lambda: self.display_inventory_field('Yes'))
        self.track_inventory_n.clicked.connect(lambda: self.display_inventory_field('No'))

        self.save_item_button.clicked.connect(lambda: self.step_a(self.item_name_field, self.barcode_field, self.expire_dt_field, self.item_type_field, self.brand_field, self.sales_group_field, self.supplier_field, self.cost_field, self.discount_field, self.sell_price_field, self.effective_dt_field))

        self.layout.addWidget(self.item_name_field)
        self.layout.addWidget(self.barcode_field)
        self.layout.addWidget(self.expire_dt_field)
        self.layout.addWidget(self.item_type_field)
        self.layout.addWidget(self.brand_field)
        self.layout.addWidget(self.sales_group_field)
        self.layout.addWidget(self.supplier_field)
        self.layout.addWidget(self.cost_field)
        self.layout.addWidget(self.discount_field)
        self.layout.addWidget(self.sell_price_field)
        self.layout.addWidget(self.effective_dt_field)
        self.layout.addWidget(self.track_inventory)
        self.layout.addWidget(self.track_inventory_y)
        self.layout.addWidget(self.track_inventory_n)
        self.layout.addWidget(self.on_hand_stock_field)
        self.layout.addWidget(self.available_stock_field)
        self.layout.addWidget(self.spacer)
        self.layout.addWidget(self.save_item_button)

        self.setLayout(self.layout)

class ListItemTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.retrieve_query = RetrieveData()
        self.create_layout()

    def open_edit_item_window(self, row_index, row_value):
        open_window = EditItemWindow(row_index, row_value)
        open_window.data_saved.connect(self.display_item_list)
        open_window.exec()

    def display_item_list(self):
        self.all_item_data = self.retrieve_query.all_item_data()

        self.setRowCount(len(self.all_item_data))

        for row_index, row_value in enumerate(self.all_item_data):
            for column_index, column_value in enumerate(row_value):
                self.setItem(row_index, column_index + 1, QTableWidgetItem(str(column_value)))
            edit_item_button = QPushButton('EDIT')
            edit_item_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.open_edit_item_window(row_index, row_value))
            self.setCellWidget(row_index, 0, edit_item_button)

    def create_layout(self):
        self.setColumnCount(12)
        self.setHorizontalHeaderLabels(['','Item name','Barcode','Expire date','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Effective date'])

        self.display_item_list()

class ItemManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.create_layout()

    def open_add_item_window(self):
        list_item_table = ListItemTable()

        open_window = AddItemWindow()
        open_window.data_saved.connect(self.list_item_table.display_item_list)
        open_window.exec()

    def create_layout(self):
        self.layout = QGridLayout()

        self.filter_item_field = QLineEdit()
        self.add_item_button = QPushButton('ADD ITEM')

        self.list_item_table = ListItemTable()

        self.add_item_button.clicked.connect(self.open_add_item_window)

        self.layout.addWidget(self.filter_item_field,0,0)
        self.layout.addWidget(self.add_item_button,0,1)
        self.layout.addWidget(self.list_item_table,1,0,1,2)

        self.setLayout(self.layout)
