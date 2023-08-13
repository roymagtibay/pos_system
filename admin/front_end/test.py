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

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemEditor()
    window.show()
    sys.exit(app.exec())



