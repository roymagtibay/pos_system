import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

from add_item import *

class ItemManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Item Management')
        self.setGeometry(1000,100,300,300)

        self.add_item = AddItem()

        self.create_body()
    
    def create_body(self):
        self.layout = QGridLayout()

        filter_item_field = QLineEdit()
        add_item_button = QPushButton('ADD ITEM')
        item_list_table = QTableWidget()

        add_item_button.clicked.connect(self.open_add_item_window)

        self.layout.addWidget(filter_item_field,0,0)
        self.layout.addWidget(add_item_button,0,1)
        self.layout.addWidget(item_list_table,1,0,1,2)

        self.setLayout(self.layout)

    def open_add_item_window(self):
        self.add_item.exec()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagement()
    window.show()
    sys.exit(pos_app.exec())