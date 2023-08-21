import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.inventory_management_sql import *

class InventoryManagementWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Inventory Management')
        self.create_table = CreateDatabaseTable()
        self.create_table.database_table()
        self.init_layout()

    # filter stock flag
    def filter_stock(self):
        filter_input = self.filter_stock_field.text()

        if filter_input == '':
            self.list_stock_table.display_stock_table(filter_input)
        else:
            self.list_stock_table.filter_stock_table(filter_input)

    def init_layout(self):
        self.layout = QGridLayout()

        self.filter_stock_field = QLineEdit()
        self.filter_stock_field.setPlaceholderText('Filter stock by stock name, supplier, etc...')

        self.list_stock_table = ListInventoryTable() # -- class ListInventoryTable(QTableWidget)

        self.filter_stock_field.textChanged.connect(self.filter_stock) # connects to filter_stock functions every change of text

        self.layout.addWidget(self.filter_stock_field,0,0)
        self.layout.addWidget(self.list_stock_table,1,0)

        self.setLayout(self.layout)

class EditStockDialog(QDialog):
    data_saved = pyqtSignal()

    def __init__(self, row_index, row_value):
        super().__init__()

        self.call_sql_utils()
        self.init_layout(row_index, row_value)

    def call_sql_utils(self):
        self.update_stock = UpdateStockData()
        self.select_stock = SelectStockData()

    def init_layout(self, row_index, row_value):
        self.layout = QGridLayout()

        self.numeric_input_validator = QDoubleValidator()
        self.numeric_input_validator.setDecimals(0)  # Set the number of decimal places
        self.numeric_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.numeric_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

        self.on_hand_stock = QLineEdit()
        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.on_hand_stock.setValidator(self.numeric_input_validator)
        self.available_stock = QLineEdit()
        self.available_stock.setPlaceholderText('Available stock')
        self.available_stock.setValidator(self.numeric_input_validator)

        self.save_button = QPushButton('SAVE')

 
        self.on_hand_stock.setText(str(row_value[2]))
        self.available_stock.setText(str(row_value[3]))

        self.save_button.clicked.connect(lambda: self.step_a(self.on_hand_stock, self.available_stock, row_value))

        self.layout.addWidget(self.on_hand_stock)
        self.layout.addWidget(self.available_stock)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def step_a(self, raw_on_hand_stock, raw_available_stock, row_value):
        raw_supplier_id = str(row_value[4])
        raw_item_id = str(row_value[5])

        converted_supplier_id = int(raw_supplier_id)
        converted_item_id = int(raw_item_id)
        converted_on_hand_stock = int(raw_on_hand_stock.text())
        converted_available_stock = int(raw_available_stock.text())

        self.step_b(converted_supplier_id, converted_item_id, converted_on_hand_stock, converted_available_stock)

    def step_b(self, converted_supplier_id, converted_item_id, converted_on_hand_stock, converted_available_stock):
        print(converted_supplier_id)
        print(converted_item_id)
        print(converted_on_hand_stock)
        print(converted_available_stock)
        
        self.update_stock.stock_data(converted_on_hand_stock, converted_available_stock, converted_supplier_id, converted_item_id)

        self.data_saved.emit()
        self.accept()

class ListInventoryTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.call_sql_utils()
        self.init_layout()

    # call sql queries 
    def call_sql_utils(self):
        self.select_stock = SelectStockData()

    # call 'EditStockDialog(QDialog)'
    def open_edit_stock_window(self, row_index, row_value):
        edit_stock_dialog = EditStockDialog(row_index, row_value)
        edit_stock_dialog.data_saved.connect(lambda: self.display_stock_table(''))
        edit_stock_dialog.exec()

    # displays filtered stocks
    def filter_stock_table(self, filter_text):
        filtered_stock_data = self.select_stock.filtered_stock_data(filter_text)

        self.setRowCount(len(filtered_stock_data))
        
        for row_index, row_value in enumerate(filtered_stock_data):
            row_cell_limit = row_value[:4] # limits the data shown in the table

            for col_index, col_value in enumerate(row_cell_limit):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))

            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.open_edit_stock_window(row_index, row_value))
            self.setCellWidget(row_index, 0, self.edit_tem_button)

    # displays 50 recently added stocks
    def display_stock_table(self, text):
        all_stock_data = self.select_stock.all_stock_data(text)

        self.setRowCount(50)
        
        for row_index, row_value in enumerate(all_stock_data):
            row_cell_limit = row_value[:4] # limits the data shown in the table

            for col_index, col_value in enumerate(row_cell_limit):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))

            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, row_value=row_value: self.open_edit_stock_window(row_index, row_value))
            self.setCellWidget(row_index, 0, self.edit_tem_button)

    # main layout of 'ListInventoryTable(QTableWidget)'
    def init_layout(self):
        
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['','Supplier','Item name','On hand stock','Available stock'])
        
        # sets the value of the parameter of display_stock_table function to ''
        self.display_stock_table('')
        
if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = InventoryManagementWidget()
    window.show()
    sys.exit(pos_app.exec())
