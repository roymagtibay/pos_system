import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.init_db_manager import *

from item_management import ItemManagement
from inventory_management import InventoryManagement
from promo_management import PromoManagement
from customer_management import CustomerManagement

class AdminMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(700, 100, 600, 600)
        self.setWindowTitle('POS System (Admin)')

        self.create_table = InitDatabaseTable()
        self.create_table.database_table()

        self.create_layout()

    def change_content_tab(self, index):
        self.content_container.setCurrentIndex(index)

    def display_content(self):
        self.content_container = QStackedWidget()

        self.content_container.setCurrentIndex(0)

        item_management_tab = ItemManagement()
        inventory_management_tab = InventoryManagement()
        promo_management_tab = PromoManagement()
        customer_management_tab = CustomerManagement()

        self.content_container.addWidget(item_management_tab)
        self.content_container.addWidget(inventory_management_tab)
        self.content_container.addWidget(promo_management_tab)
        self.content_container.addWidget(customer_management_tab)
        # self.content_container.addWidget()
        # self.content_container.addWidget()

        return self.content_container

    def display_navbar(self):
        self.navbar_container = QGroupBox()
        self.navbar_layout = QVBoxLayout()

        item_management = QPushButton('Item')
        inventory_management = QPushButton('Inventory')
        customer_management = QPushButton('Customer')
        promo_management = QPushButton('Promo')
        user_management = QPushButton('User')
        settings = QPushButton('Settings')
        spacer = QFrame()

        item_management.clicked.connect(lambda: self.change_content_tab(0))
        inventory_management.clicked.connect(lambda: self.change_content_tab(1))
        promo_management.clicked.connect(lambda: self.change_content_tab(2))
        customer_management.clicked.connect(lambda: self.change_content_tab(3))
        user_management.clicked.connect(lambda: self.change_content_tab(4))
        settings.clicked.connect(lambda: self.change_content_tab(5))

        self.navbar_layout.addWidget(item_management)
        self.navbar_layout.addWidget(inventory_management)
        self.navbar_layout.addWidget(promo_management)
        self.navbar_layout.addWidget(customer_management)
        self.navbar_layout.addWidget(user_management)
        self.navbar_layout.addWidget(settings)
        self.navbar_layout.addWidget(spacer)

        self.navbar_container.setLayout(self.navbar_layout)

        return self.navbar_container

    def create_layout(self):
        self.layout = QGridLayout()
        
        navbar = self.display_navbar()
        content = self.display_content()

        self.layout.addWidget(navbar,0,0)
        self.layout.addWidget(content,0,1)

        self.setLayout(self.layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = AdminMainWindow()
    window.show()
    sys.exit(pos_app.exec())