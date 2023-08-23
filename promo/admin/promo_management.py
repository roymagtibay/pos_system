import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.promo_management_sql import *

class PromoManagementWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Promo Management')
        self.create_table = CreateDatabaseTable()
        self.create_table.database_table()
        self.init_layout()

    # filter Promo flag
    def filter_Promo(self):
        filter_input = self.filter_Promo_field.text()

        if filter_input == '':
            self.list_Promo_table.display_Promo_table(filter_input)
        else:
            self.list_Promo_table.filter_Promo_table(filter_input)

    def init_layout(self):
        self.layout = QGridLayout()

        self.filter_Promo_field = QLineEdit()
        self.filter_Promo_field.setPlaceholderText('Filter Promo by Promo name, supplier, etc...')

        self.add_promo_button = QPushButton('ADD')


        self.list_Promo_table = PromoListTable() # -- class ListPromoTable(QTableWidget)

        self.filter_Promo_field.textChanged.connect(self.filter_Promo) # connects to filter_Promo functions every change of text
        self.add_promo_button.clicked.connect(lambda: self.list_Promo_table.save_Promo_window("", "", "", "",""))

        self.layout.addWidget(self.filter_Promo_field,0,0)
        self.layout.addWidget(self.add_promo_button,0,1)
        self.layout.addWidget(self.list_Promo_table,1,0,1,2)

        self.setLayout(self.layout)

class PromoListTable(QTableWidget):
    data_saved = pyqtSignal()
    def __init__(self):
        super().__init__()       
        self.call_sql_utils()
        self.init_layout()

    def call_sql_utils(self):
        self.PromoSelect = SelectPromoData()
        self.update_Promo = UpdatePromoData()

    def init_layout(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["","Promo Name", "Description", "Type", "Value"])
        
        self.populate_PromoList()
    
    def populate_PromoList(self):
        self.clearContents()

        data = self.PromoSelect.all_Promo_data()

        self.setRowCount(len(data))    

        for row_index, (Promo_name, Promo_desc, promo_type, promo_value) in enumerate(data):
            self.setItem(row_index, 1, QTableWidgetItem(str(Promo_name)))
            self.setItem(row_index, 2, QTableWidgetItem(str(Promo_desc)))
            self.setItem(row_index, 3, QTableWidgetItem(str(promo_type)))
            self.setItem(row_index, 4, QTableWidgetItem(str(promo_value)))
            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, Promo_name=Promo_name, Promo_desc=Promo_desc, Promo_type=promo_type, Promo_value=promo_value : self.save_Promo_window(row_index, Promo_name, Promo_desc, Promo_type, Promo_value))
            self.setCellWidget(row_index, 0, self.edit_tem_button)    

    def save_Promo_window(self, row_index, Promo_name, Promo_desc, Promo_type, Promo_value):
        edit_item_dialog = SavePromoDialog(row_index, Promo_name, Promo_desc, Promo_type, Promo_value)
        edit_item_dialog.exec()
        self.populate_PromoList()

        self.data_saved.emit()

class SavePromoDialog(QDialog):
    data_saved = pyqtSignal()
    def __init__(self, row_index, Promo_name, Promo_desc, Promo_type, Promo_value):
        super().__init__()
        self.newPromo=""

        self.call_sql_utils()
        self.init_layout(row_index, Promo_name, Promo_desc, Promo_type, Promo_value)

    def call_sql_utils(self):
        self.promo_data = InsertPromoData()
        self.update_Promo = UpdatePromoData()

    def init_layout(self, row_index, Promo_name, Promo_desc, Promo_type, Promo_value):
        self.layout = QGridLayout()

        self.numeric_input_validator = QDoubleValidator()
        self.numeric_input_validator.setDecimals(2)  # Set the number of decimal places
        self.numeric_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.numeric_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

        NameLbl = QLabel("Promo Name ")

        self.NameVal = QLineEdit()
        self.NameVal.setText(str(Promo_name))

        PromoDescLbl = QLabel("Description ")
        self.PromoDescVal = QLineEdit()
        self.PromoDescVal.setText(str(Promo_desc))

        
        PromoTypeLbl = QLabel("Promo Type ")
        self.PromoTypeVal = QLineEdit()
        self.PromoTypeVal.setText(str(Promo_type))
        
        PromoValLbl = QLabel("Promo Value ")
        self.PromoVal = QLineEdit()
        self.PromoVal.setText(str(Promo_value))
        self.PromoVal.setValidator(self.numeric_input_validator)
        
        save_button = QPushButton('SAVE')

        save_button.clicked.connect(lambda: self.Save_Promo(Promo_name))

        self.layout.addWidget(NameLbl,0,0)
        self.layout.addWidget(self.NameVal,0,1)
        self.layout.addWidget(PromoDescLbl,1,0)
        self.layout.addWidget(self.PromoDescVal,1,1)
        self.layout.addWidget(PromoTypeLbl,2,0)
        self.layout.addWidget(self.PromoTypeVal,2,1)
        self.layout.addWidget(PromoValLbl,3,0)
        self.layout.addWidget(self.PromoVal,3,1)

        self.layout.addWidget(save_button,4,1)

        self.setLayout(self.layout)

    def Save_Promo(self, Promo_name):
        newPromo = self.NameVal.text()
        newDesc = self.PromoDescVal.text()
        newTpye = self.PromoTypeVal.text()
        newVal = self.PromoVal.text()

        if Promo_name == "":
            self.promo_data.InsertPromo(newPromo, newDesc, newTpye, newVal)
        else:
            self.update_Promo.promo_data(newPromo, newDesc, newTpye, newVal, Promo_name)
        self.close()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = PromoManagementWidget()
    window.show()
    sys.exit(pos_app.exec())
