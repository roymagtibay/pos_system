import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

class ItemEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Item Editor")
        self.setGeometry(100, 100, 800, 400)

        self.init_ui()

        self.conn = sqlite3.connect("items.db")
        self.create_tables()

    def init_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.color_input = QLineEdit()  # Added color input
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)

        layout.addWidget(QLabel("Product Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Color:"))  # Added label for color
        layout.addWidget(self.color_input)   # Added color input
        layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Product Name", "Color", "Edit"])
        layout.addWidget(QLabel("Products"))
        layout.addWidget(self.table)

        main_widget.setLayout(layout)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, color TEXT)")
        self.conn.commit()

    def add_product(self):
        name = self.name_input.text()
        color = self.color_input.text()  # Get color input
        if name and color:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO items (name, color) VALUES (?, ?)", (name, color))  # Insert color
            self.conn.commit()
            self.name_input.clear()
            self.color_input.clear()  # Clear color input
            self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        for row_number, item in enumerate(items):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(item):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, row=row_number, item=item: self.edit_item(row, item))
            self.table.setCellWidget(row_number, 3, edit_button)

    def edit_item(self, row, item):
        item_id = int(item[0])
        current_name = item[1]
        current_color = item[2]  # Get the color from the tuple

        new_name, ok_name = QInputDialog.getText(self, "Edit Product", "Enter new product name:", text=current_name)
        new_color, ok_color = QInputDialog.getText(self, "Edit Product", "Enter new color:", text=current_color)  # Get the new color
        if ok_name and new_name.strip() and ok_color and new_color.strip():  # Check both inputs
            cursor = self.conn.cursor()
            cursor.execute("UPDATE items SET name = ?, color = ? WHERE id = ?", (new_name, new_color, item_id))  # Update color
            self.conn.commit()
            self.update_table()

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemEditor()
    window.show()
    sys.exit(app.exec())



# import sqlite3
# import sys, os
# from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *
# from PyQt6.QtGui import *
# from PyQt6 import *

# from add_item import AddItem
# from edit_item import EditItem
# from salesdb import SalesDBFunctions

# class ProductManagement(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.create_content()
#         self.show_item_list()  # Call this method to populate the table with data

#         self.add_item_push_button.clicked.connect(self.show_add_item)



    
#     def show_item_list(self):
#         self.salesdb_functions = SalesDBFunctions()

#         self.conn = sqlite3.connect('SALES.db')
#         self.cursor = self.conn.cursor()

#         self.salesdb_functions.create_item_table()
#         self.salesdb_functions.create_item_type_table()
#         self.salesdb_functions.create_item_brand_table()
#         self.salesdb_functions.create_supplier_table()
#         self.salesdb_functions.create_sales_group_table()
#         self.salesdb_functions.create_item_price_table()

#         # Query for the 'Item' table
#         self.cursor.execute('SELECT ItemName, Barcode, ExpireDt FROM Item')
#         item_data = self.cursor.fetchall()

#         # Query for other tables (Assuming you have 'ItemType' and 'Brand' tables)
#         self.cursor.execute('SELECT Name FROM ItemType')
#         item_type_data = self.cursor.fetchall()

#         self.cursor.execute('SELECT Name FROM Brand')
#         brand_data = self.cursor.fetchall()

#         self.cursor.execute('SELECT Name FROM Supplier')
#         supplier_data = self.cursor.fetchall()

#         self.cursor.execute('SELECT Name FROM SalesGroup')
#         sales_group_data = self.cursor.fetchall()

#         self.cursor.execute('SELECT Cost, Discount, SellPrice, EffectiveDt FROM ItemPrice')
#         item_price_data = self.cursor.fetchall()

#         # Determine the maximum number of rows needed for the table
#         max_rows = max(len(item_data), len(item_type_data), len(brand_data))
#         self.item_list_table.setRowCount(max_rows)

#         # Populate the table with data
#         for row_num in range(max_rows):
#             item_name, barcode, expiry_date = item_data[row_num] if row_num < len(item_data) else ("","","")
#             item_type = item_type_data[row_num][0] if row_num < len(item_type_data) else ""
#             brand = brand_data[row_num][0] if row_num < len(brand_data) else ""
#             supplier = supplier_data[row_num][0] if row_num < len(supplier_data) else ""
#             sales_group = sales_group_data[row_num][0] if row_num < len(sales_group_data) else ""
#             cost, discount, sell_price, effective_date = item_price_data[row_num] if row_num < len(item_price_data) else ("","","","")

#             # Populate the cells with the retrieved data
#             self.edit_push_button = QPushButton('EDIT')
#             self.edit_push_button.clicked.connect(self.show_edit_item)
#             self.item_list_table.setCellWidget(row_num, 0, self.edit_push_button)

#             self.item_list_table.setItem(row_num, 1, QTableWidgetItem(item_name))
#             self.item_list_table.setItem(row_num, 2, QTableWidgetItem(barcode))
#             self.item_list_table.setItem(row_num, 3, QTableWidgetItem(item_type))
#             self.item_list_table.setItem(row_num, 4, QTableWidgetItem(brand))
#             self.item_list_table.setItem(row_num, 5, QTableWidgetItem(supplier))
#             self.item_list_table.setItem(row_num, 6, QTableWidgetItem(sales_group))
#             self.item_list_table.setItem(row_num, 7, QTableWidgetItem(str(cost)))
#             self.item_list_table.setItem(row_num, 8, QTableWidgetItem(str(discount)))
#             self.item_list_table.setItem(row_num, 9, QTableWidgetItem(str(sell_price)))
#             self.item_list_table.setItem(row_num, 10, QTableWidgetItem(expiry_date))
#             self.item_list_table.setItem(row_num, 11, QTableWidgetItem(effective_date))

#         self.conn.close()


#     def show_add_item(self):
#         self.add_item_dialogue = AddItem()
#         self.add_item_dialogue.data_saved.connect(self.show_item_list)
#         self.add_item_dialogue.exec()

#     def show_edit_item(self):
#         # Get the sender of the signal, which is the clicked "Edit" button
#         self.edit_button = self.sender()

#         # Get the row index of the clicked "Edit" button
#         row_index = self.item_list_table.indexAt(self.edit_button.pos()).row()

#         # Get the data for the selected row
#         self.item_name = self.item_list_table.item(row_index, 1).text()
#         self.barcode = self.item_list_table.item(row_index, 2).text()
#         self.item_type = self.item_list_table.item(row_index, 3).text()
#         self.brand = self.item_list_table.item(row_index, 4).text()
#         self.supplier = self.item_list_table.item(row_index, 5).text()
#         self.sales_group = self.item_list_table.item(row_index, 6).text()
#         self.item_cost = float(self.item_list_table.item(row_index, 7).text())
#         self.item_discount = float(self.item_list_table.item(row_index, 8).text())
#         self.item_sell_price = float(self.item_list_table.item(row_index, 9).text())
#         # Handle date format conversion (assuming date cells use ISODate format)
#         self.expiry_date_item = self.item_list_table.item(row_index, 10)
#         self.expiry_date = QDate.fromString(self.expiry_date_item.text(), Qt.DateFormat.ISODate) if self.expiry_date_item else QDate.currentDate()
        
#         self.effective_date_item = self.item_list_table.item(row_index, 11)
#         self.effective_date = QDate.fromString(self.effective_date_item.text(), Qt.DateFormat.ISODate) if self.effective_date_item else QDate.currentDate()

#         # Create an instance of the EditItem dialog and pass the data
#         self.edit_item_dialogue = EditItem()

#         self.edit_item_dialogue.item_name.setText(self.item_name)
#         self.edit_item_dialogue.barcode.setText(self.barcode)
#         self.edit_item_dialogue.item_type.setCurrentText(self.item_type)
#         self.edit_item_dialogue.brand.setCurrentText(self.brand)
#         self.edit_item_dialogue.supplier.setCurrentText(self.supplier)
#         self.edit_item_dialogue.sales_group.setCurrentText(self.sales_group)
#         self.edit_item_dialogue.item_cost.setText(str(self.item_cost))
#         self.edit_item_dialogue.item_discount.setText(str(self.item_discount))
#         self.edit_item_dialogue.item_sell_price.setText(str(self.item_sell_price))
#         self.edit_item_dialogue.expiry_date.setDate(self.expiry_date)
#         self.edit_item_dialogue.effective_date.setDate(self.effective_date)


#         # Connect the data_saved signal to refresh the item list after saving
#         self.edit_item_dialogue.data_saved.connect(self.show_item_list)

#         # Show the dialog
#         self.edit_item_dialogue.exec()

#     def create_content(self):
        
#         self.grid_layout = QGridLayout()
        
#         # primary information
#         self.filter_item = QLineEdit()
#         self.add_item_push_button = QPushButton('ADD ITEM')
#         self.add_item_push_button.clicked.connect(self.show_add_item)

#         self.item_list_table = QTableWidget()
#         self.item_list_table.setColumnCount(12)
#         self.item_list_table.setHorizontalHeaderLabels(['Item name','Barcode','Item type','Brand','Supplier','Sales group','Cost','Discount','Sell price','Expiry date','Effective date'])

#         self.grid_layout.addWidget(self.filter_item, 0, 0)
#         self.grid_layout.addWidget(self.add_item_push_button, 0, 1)
#         self.grid_layout.addWidget(self.item_list_table, 1, 0, 2, 2)

#         self.setLayout(self.grid_layout)

# if __name__ == ('__main__'):
#     pos_app = QApplication(sys.argv)
#     window = ProductManagement()
#     window.show()
#     sys.exit(pos_app.exec())