import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.init_db_manager import *
from utils.customer_db_manager import *

class CustomerManagement(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(300)

        self.manage_customer_data = ManageCustomerData()

        self.create_layout()

        # self.customer_name_field.setCurrentText(customer_data)
        # self.address_field.setText()
        # self.barrio_field.setCurrentText()
        # self.town_field.setCurrentText()
        # self.phone_field.setText()
        # self.age_field.setText()
        # self.gender_field.setCurrentText()
        # self.marital_status_field.setCurrentText()

    def store_customer_data(self, raw_customer_name, raw_address, raw_barrio, raw_town, raw_phone, raw_age, raw_gender, raw_marital_status):
        converted_customer_customer_name = str(raw_customer_name.currentText())
        converted_customer_address = str(raw_address.text())
        converted_customer_barrio = str(raw_barrio.text())
        converted_customer_town = str(raw_town.text())
        converted_customer_phone = str(raw_phone.text())
        converted_customer_age = str(raw_age.text())
        converted_customer_gender = str(raw_gender.currentText())
        converted_customer_marital_status = str(raw_marital_status.currentText())

        self.manage_customer_data.store_all_data(converted_customer_customer_name, converted_customer_address, converted_customer_barrio, converted_customer_town, converted_customer_phone, converted_customer_age, converted_customer_gender, converted_customer_marital_status)

        self.manage_customer_data.change_all_data(converted_customer_customer_name, converted_customer_address, converted_customer_barrio, converted_customer_town, converted_customer_phone, converted_customer_age, converted_customer_gender, converted_customer_marital_status)

        customer_data = self.manage_customer_data.retreive_all_data(converted_customer_customer_name)

        print('ITEM ID: ', customer_data)

    def test_function(self, raw_customer_name):
        os.system('cls')
        print('RAW: ', raw_customer_name)

        converted_customer_customer_name = str(raw_customer_name.currentText())

        print('CONVERTED: ', converted_customer_customer_name)

        customer_id_data = self.manage_customer_data.retreive_all_data(converted_customer_customer_name)

        print('PRINT ALL: ', customer_id_data)


        

    def create_layout(self):
        self.layout = QGridLayout()

        self.customer_name_field = QComboBox()
        self.address_field = QLineEdit()
        self.barrio_field = QLineEdit()
        self.town_field = QLineEdit()
        self.phone_field = QLineEdit()
        self.age_field = QLineEdit()
        self.gender_field = QComboBox()
        self.marital_status_field = QComboBox()
        self.save_customer_button = QPushButton('SAVE CUSTOMER')
        self.test = QPushButton('TEST')

        self.address_field.setPlaceholderText('Address')
        self.barrio_field.setPlaceholderText('Barrio')
        self.town_field.setPlaceholderText('Town')
        self.phone_field.setPlaceholderText('Phone')
        self.age_field.setPlaceholderText('Age')

        self.customer_name_field.setEditable(True)

        self.gender_field.addItem('Male')
        self.gender_field.addItem('Female')

        self.marital_status_field.addItem('Single')
        self.marital_status_field.addItem('Married')
        self.marital_status_field.addItem('Separated')
        self.marital_status_field.addItem('Widowed')


        converted_customer_customer_name = str(self.customer_name_field.currentText())

        customer_id_data = self.manage_customer_data.retreive_all_data(converted_customer_customer_name)
        
        for row in customer_id_data:
            print('customer_id_data: ', row[0])

            self.address_field.setText(row[1])
            self.barrio_field.setText(row[2])
            self.town_field.setText(row[3])
            self.phone_field.setText(row[4])
            self.age_field.setText(row[5])
            self.gender_field.setCurrentText(row[6])
            self.marital_status_field.setCurrentText(row[7])


        self.save_customer_button.clicked.connect(lambda: self.store_customer_data(self.customer_name_field, self.address_field, self.barrio_field, self.town_field, self.phone_field, self.age_field, self.gender_field, self.marital_status_field))

        self.test.clicked.connect(lambda: self.test_function(self.customer_name_field))

        self.layout.addWidget(self.customer_name_field)
        self.layout.addWidget(self.address_field)
        self.layout.addWidget(self.barrio_field)
        self.layout.addWidget(self.town_field)
        self.layout.addWidget(self.phone_field)
        self.layout.addWidget(self.age_field)
        self.layout.addWidget(self.gender_field)
        self.layout.addWidget(self.marital_status_field)
        self.layout.addWidget(self.save_customer_button)
        self.layout.addWidget(self.test)

        self.setLayout(self.layout)
