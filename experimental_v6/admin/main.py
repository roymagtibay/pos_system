import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from item_manangement import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

    def init_layout(self):
        self.layout = QGridLayout()

        self.setLayout(self.layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(pos_app.exec())
