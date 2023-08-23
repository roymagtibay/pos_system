import sys, os
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox, QWidget, QLineEdit, QPushButton, QMessageBox, QFormLayout, QLabel, QTextEdit
from PyQt6.QtCore import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.customer_management_sql import *

class CustomerMngt(QMainWindow):
    data_saved = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.InitDatabaseTable = CreateDatabaseTable()
        self.CustomerData = CustomerData()
        self.setWindowTitle("Customer Management")
        self.setFixedSize(600, 400)  # Set window position and size

        self.init_db()
        self.init_ui()

    def init_db(self):
        self.InitDatabaseTable.database_table()
        
    def init_ui(self):

        central_widget = QWidget()  # Create a central widget to hold the layout
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        form_layout = QFormLayout()  # Form layout for label and combobox
        layout.addLayout(form_layout)

         # Create label and combobox
        customer_name = QLabel("Customer Name :")
        customer_address = QLabel("Address :")
        customer_barrio = QLabel("Barangay :")
        customer_town = QLabel("Town/City :")
        customer_phone = QLabel("Phone :")
        customer_age = QLabel("Age :")
        customer_gender = QLabel("Gender :", alignment=Qt.AlignmentFlag.AlignRight)
        customer_marital = QLabel("Marital Status :")


        customer_name.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_address.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_barrio.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_town.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_phone.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_age.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_gender.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')
        customer_marital.setStyleSheet(''' font-size: 16px; color:rgb(25,25,112)''')


        self.combo_box = QComboBox(self)
        self.combo_box.setEditable(True)
        cusname = self.combo_box
        

        address_field = QTextEdit()
        address_field.setFixedSize(455, 60)
        barrio_field = QLineEdit()
        town_field = QLineEdit()
        phone_field = QLineEdit()
        age_field = QLineEdit()
        gender_field = QComboBox(self)
        gender_field.addItem("M")
        gender_field.addItem("F")
        marital_field = QComboBox(self)
        marital_field.addItem('S')
        marital_field.addItem('M')
        marital_field.addItem('W')

        self.address_field = address_field
        self.barrio_field = barrio_field
        self.town_field = town_field
        self.phone_field = phone_field
        self.age_field = age_field
        self.gender_field = gender_field
        self.marital_field = marital_field

        form_layout.addRow(customer_name, self.combo_box)
        form_layout.addRow(customer_address, address_field)
        form_layout.addRow(customer_barrio, barrio_field)
        form_layout.addRow(customer_town, town_field)
        form_layout.addRow(customer_phone, phone_field)
        form_layout.addRow(customer_age, age_field)
        form_layout.addRow(customer_gender, gender_field)
        form_layout.addRow(customer_marital, marital_field)
   
        self.save_button = QPushButton("Save", self)
        self.save_button.setFixedSize(200, 50)
        self.save_button.setStyleSheet("background-color: rgb(179,238,238);")
        self.save_button.clicked.connect(lambda: self.save_to_database(cusname, address_field, barrio_field, town_field, phone_field, age_field, gender_field, marital_field))
        layout.addWidget(self.save_button)
        layout.setAlignment(self.save_button, Qt.AlignmentFlag.AlignHCenter)

        self.close_button = QPushButton("Close", self)
        self.close_button.setFixedSize(200, 50)
        self.close_button.setStyleSheet("background-color: rgb(240,230,140);")
        layout.addWidget(self.close_button)
        layout.setAlignment(self.close_button, Qt.AlignmentFlag.AlignHCenter)
        self.close_button.clicked.connect(self.close_window)

        #self.connection = sqlite3.connect('C:/Users/User/pos_system-main/pos_system-main/experimental_v3/sales/sales.db')
        #self.cursor = self.connection.cursor()

        self.delay_timer = QTimer(self)
        self.delay_timer.setInterval(1000)  # 1000 milliseconds (1 seconds)
        self.delay_timer.setSingleShot(True)
        self.delay_timer.start()
        self.delay_timer.timeout.connect(self.delayed_filter)
        

    def close_window(self):
        self.close()

    def load_Details(self, name):
        data = self.CustomerData.FetchDataByName(name)
        address_line = data[0]
        barrio_line = data[1]
        town_line = data[2]
        phone_line = data[3]
        age_line = str(data[4])
        gender_line = data[5]
        marital_line = data[6]
        self.address_field.setText(address_line)
        self.barrio_field.setText(barrio_line)
        self.town_field.setText(town_line)
        self.phone_field.setText(phone_line)
        self.age_field.setText(age_line)
        self.gender_field.setCurrentText(gender_line)
        self.marital_field.setCurrentText(marital_line)
        

    def filter_names(self):
        self.delay_timer.stop()  # Reset the timer
        self.delay_timer.start()  # Start the timer
        

    def delayed_filter(self):
        
        self.combo_box.lineEdit().textChanged.connect(self.filter_names)
        text = self.combo_box.currentText()
        if text:
            print(text)
            names = self.CustomerData.SelectLikeNames(text)
            if names:
                filtered_names = [item[0] for item in names]
                cnt = len(filtered_names)
    
                self.combo_box.clear()  # Clear previous items
                self.combo_box.addItems(filtered_names)  # Populate ComboBox with filtered items
    
                 #self.combo_box.lineEdit().setText(text)  # Restore user input
                  # Show the ComboBox dropdown
    
                print("xxx")
                print(cnt)
                if cnt > 0:
                    self.combo_box.showPopup()
                    self.load_Details(filtered_names[0])
                    self.combo_box.lineEdit().setText(text)
                    
    
                self.delay_timer.stop()   
        else:
            self.address_field.setText('')
            self.barrio_field.setText('')
            self.town_field.setText('')
            self.phone_field.setText('')
            self.age_field.setText('')
            self.gender_field.setCurrentText('')
            self.marital_field.setCurrentText('')
            self.delay_timer.stop()
            
        self.combo_box.hidePopup() 
        self.combo_box.setEditText(text)   
        print("bbb")
        self.combo_box.lineEdit().setCursorPosition(len(self.combo_box.currentText()))


    def save_to_database(self, name, address, barrio, town, phone, age, gender, marital):
        name_data = name.lineEdit().text()
        address_data = str(address.toPlainText())
        barrio_data = str(barrio.text())
        town_data = str(town.text())
        phone_data = str(phone.text())
        age_data = str(age.text())
        gender_data = str(gender.currentText())
        marital_data = str(marital.currentText())

        if name_data:
            #self.cursor.execute("SELECT Fullname, Address, Barrio, Town, Phone, Age, Gender, Marital_Status FROM Customer WHERE Fullname = ?", (name_data, ))
            cust_record = self.CustomerData.FetchDataByName(name_data)

            if not cust_record:
                self.CustomerData.Insertdata(name_data, address_data, barrio_data, town_data, phone_data, age_data, gender_data, marital_data)
                QMessageBox.information(self, "Success", "Customer saved successfully.")
            else:
                self.CustomerData.Updatedata(name_data, address_data, barrio_data, town_data, phone_data, age_data, gender_data, marital_data)
                QMessageBox.information(self, "Success", "Customer updated successfully.")
        else:
            QMessageBox.warning(self, "Error", "Customer name is required.")        

    def closeEvent(self, event):
        self.close()

class CustomComboBox(QComboBox):
    def showPopup(self):
        super().showPopup()
        self.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomerMngt()

    window.show()
    sys.exit(app.exec())
