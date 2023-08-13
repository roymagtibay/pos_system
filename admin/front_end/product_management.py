import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from add_item import AddItem
from edit_item import EditItem
from salesdb import SalesDBFunctions

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()

        self.create_content()
        self.show_item_list()  # Call this method to populate the table with data

    
    def show_item_list(self):
        self.salesdb_functions = SalesDBFunctions()

        self.conn = sqlite3.connect('SALES.db')
        self.cursor = self.conn.cursor()

        self.salesdb_functions.create_item_table()
        self.salesdb_functions.create_item_type_table()
        self.salesdb_functions.create_item_brand_table()
        self.salesdb_functions.create_supplier_table()
        self.salesdb_functions.create_sales_group_table()
        self.salesdb_functions.create_item_price_table()

        # Query for the 'Item' table
        self.cursor.execute('SELECT ItemName, Barcode, ExpireDt FROM Item')
        item_data = self.cursor.fetchall()

        self.cursor.execute('SELECT Name FROM ItemType')
        item_type_data = self.cursor.fetchall()

        self.cursor.execute('SELECT Name FROM Brand')
        brand_data = self.cursor.fetchall()

        self.cursor.execute('SELECT Name FROM Supplier')
        supplier_data = self.cursor.fetchall()

        self.cursor.execute('SELECT Name FROM SalesGroup')
        sales_group_data = self.cursor.fetchall()

        self.cursor.execute('SELECT Cost, Discount, SellPrice, EffectiveDt FROM ItemPrice')
        item_price_data = self.cursor.fetchall()

        # Determine the maximum number of rows needed for the table
        max_rows = max(len(item_data), len(item_type_data), len(brand_data))
        self.item_list_table.setRowCount(max_rows)

        # Populate the table with data
        for row_num in range(max_rows):
            item_name, barcode, expiry_date = item_data[row_num] if row_num < len(item_data) else ("","","")
            item_type = item_type_data[row_num][0] if row_num < len(item_type_data) else ""
            brand = brand_data[row_num][0] if row_num < len(brand_data) else ""
            supplier = supplier_data[row_num][0] if row_num < len(supplier_data) else ""
            sales_group = sales_group_data[row_num][0] if row_num < len(sales_group_data) else ""
            cost, discount, sell_price, effective_date = item_price_data[row_num] if row_num < len(item_price_data) else ("","","","")

            # Populate the cells with the retrieved data
            self.edit_push_button = QPushButton('EDIT')
            # self.edit_push_button.clicked.connect(self.show_edit_item)
            self.item_list_table.setCellWidget(row_num, 0, self.edit_push_button)

            self.item_list_table.setItem(row_num, 1, QTableWidgetItem(item_name))
            self.item_list_table.setItem(row_num, 2, QTableWidgetItem(barcode))
            self.item_list_table.setItem(row_num, 3, QTableWidgetItem(item_type))
            self.item_list_table.setItem(row_num, 4, QTableWidgetItem(brand))
            self.item_list_table.setItem(row_num, 5, QTableWidgetItem(supplier))
            self.item_list_table.setItem(row_num, 6, QTableWidgetItem(sales_group))
            
            self.item_list_table.setItem(row_num, 7, QTableWidgetItem('{:.2f}'.format(cost)))
            self.item_list_table.item(row_num, 7).setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.item_list_table.setItem(row_num, 8, QTableWidgetItem('{:.2f}'.format(discount)))
            self.item_list_table.item(row_num, 8).setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.item_list_table.setItem(row_num, 9, QTableWidgetItem('{:.2f}'.format(sell_price)))
            self.item_list_table.item(row_num, 9).setTextAlignment(Qt.AlignmentFlag.AlignRight)
            
            self.item_list_table.setItem(row_num, 10, QTableWidgetItem(expiry_date))
            self.item_list_table.setItem(row_num, 11, QTableWidgetItem(effective_date))

        self.conn.close()


    def show_add_item(self):
        self.add_item_dialogue = AddItem()
        self.add_item_dialogue.data_saved.connect(self.show_item_list)
        self.add_item_dialogue.exec()

    def show_edit_item(self):
        # self.edit_item_dialogue = EditItem()
        # self.edit_item_dialogue.data_saved.connect(self.show_item_list)
        # self.edit_item_dialogue.exec()

        pass

    def update_table_content(self):
        filter_text = self.filter_item.text().lower()

        for row in range(self.item_list_table.rowCount()):
            item_name = self.item_list_table.item(row, 1).text().lower()
            barcode = self.item_list_table.item(row, 2).text().lower()
            item_type = self.item_list_table.item(row, 3).text().lower()
            brand = self.item_list_table.item(row, 4).text().lower()
            supplier = self.item_list_table.item(row, 5).text().lower()
            sales_group = self.item_list_table.item(row, 6).text().lower()

            if (
                filter_text in item_name
                or filter_text in barcode
                or filter_text in item_type
                or filter_text in brand
                or filter_text in supplier
                or filter_text in sales_group
            ):
                self.item_list_table.setRowHidden(row, False)
            else:
                self.item_list_table.setRowHidden(row, True)


    def create_content(self):
        
        self.grid_layout = QGridLayout()
        
        # primary information
        self.filter_item = QLineEdit()
        self.filter_item.setPlaceholderText('Filter by item name, barcode, item type, brand, supplier, etc...')
        # Inside the create_content method
        self.filter_item.textChanged.connect(self.update_table_content)

        self.add_item_push_button = QPushButton('ADD ITEM')
        self.add_item_push_button.clicked.connect(self.show_add_item)

        self.item_list_table = QTableWidget()
        self.item_list_table.setColumnCount(12)
        self.item_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.item_list_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        self.item_list_table.setHorizontalHeaderLabels(['','Item name','Barcode','Item type','Brand','Supplier','Sales group','Cost','Discount','Sell price','Expiry date','Effective date'])

        self.grid_layout.addWidget(self.filter_item, 0, 0)
        self.grid_layout.addWidget(self.add_item_push_button, 0, 1)
        self.grid_layout.addWidget(self.item_list_table, 1, 0, 2, 2)

        self.setLayout(self.grid_layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ProductManagement()
    window.show()
    sys.exit(pos_app.exec())