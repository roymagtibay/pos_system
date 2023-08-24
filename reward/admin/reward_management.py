import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.reward_management_sql import *

class RewardManagementWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Reward Management')
        self.create_table = CreateDatabaseTable()
        self.create_table.database_table()
        self.init_layout()

    # filter Reward flag
    def filter_Reward(self):
        filter_input = self.filter_Reward_field.text()

        if filter_input == '':
            self.list_Reward_table.display_Reward_table(filter_input)
        else:
            self.list_Reward_table.filter_Reward_table(filter_input)

    def init_layout(self):
        self.layout = QGridLayout()

        self.filter_Reward_field = QLineEdit()
        self.filter_Reward_field.setPlaceholderText('Filter Reward by Reward name, supplier, etc...')

        self.add_Reward_button = QPushButton('ADD')


        self.list_Reward_table = RewardListTable() # -- class ListRewardTable(QTableWidget)

        self.filter_Reward_field.textChanged.connect(self.filter_Reward) # connects to filter_Reward functions every change of text
        self.add_Reward_button.clicked.connect(lambda: self.list_Reward_table.save_Reward_window("", "", "", "",""))

        self.layout.addWidget(self.filter_Reward_field,0,0)
        self.layout.addWidget(self.add_Reward_button,0,1)
        self.layout.addWidget(self.list_Reward_table,1,0,1,2)

        self.setLayout(self.layout)

class RewardListTable(QTableWidget):
    data_saved = pyqtSignal()
    def __init__(self):
        super().__init__()       
        self.call_sql_utils()
        self.init_layout()

    def call_sql_utils(self):
        self.RewardSelect = SelectRewardData()
        self.update_Reward = UpdateRewardData()

    def init_layout(self):
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["","Reward Name", "Description", "Unit", "Point"])
        
        self.populate_RewardList()
    
    def populate_RewardList(self):
        self.clearContents()

        data = self.RewardSelect.all_Reward_data()

        self.setRowCount(len(data))    

        for row_index, (Reward_name, Reward_desc, Reward_unit, Reward_point) in enumerate(data):
            self.setItem(row_index, 1, QTableWidgetItem(str(Reward_name)))
            self.setItem(row_index, 2, QTableWidgetItem(str(Reward_desc)))
            self.setItem(row_index, 3, QTableWidgetItem(str(Reward_unit)))
            self.setItem(row_index, 4, QTableWidgetItem(str(Reward_point)))
            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, Reward_name=Reward_name, Reward_desc=Reward_desc, Reward_unit=Reward_unit, Reward_point=Reward_point : self.save_Reward_window(row_index, Reward_name, Reward_desc, Reward_unit, Reward_point))
            self.setCellWidget(row_index, 0, self.edit_tem_button)    

    def save_Reward_window(self, row_index, Reward_name, Reward_desc, Reward_unit, Reward_point):
        edit_item_dialog = SaveRewardDialog(row_index, Reward_name, Reward_desc, Reward_unit, Reward_point)
        edit_item_dialog.exec()
        self.populate_RewardList()

        self.data_saved.emit()

class SaveRewardDialog(QDialog):
    data_saved = pyqtSignal()
    def __init__(self, row_index, Reward_name, Reward_desc, Reward_unit, Reward_point):
        super().__init__()
        self.newReward=""

        self.call_sql_utils()
        self.init_layout(row_index, Reward_name, Reward_desc, Reward_unit, Reward_point)

    def call_sql_utils(self):
        self.Reward_data = InsertRewardData()
        self.update_Reward = UpdateRewardData()

    def init_layout(self, row_index, Reward_name, Reward_desc, Reward_unit, Reward_point):
        self.layout = QGridLayout()

        self.numeric_input_validator = QDoubleValidator()
        self.numeric_input_validator.setDecimals(2)  # Set the number of decimal places
        self.numeric_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.numeric_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

        NameLbl = QLabel("Reward Name ")

        self.NameVal = QLineEdit()
        self.NameVal.setText(str(Reward_name))

        RewardDescLbl = QLabel("Description ")
        self.RewardDescVal = QLineEdit()
        self.RewardDescVal.setText(str(Reward_desc))

        
        RewardTypeLbl = QLabel("Unit Value ")
        self.RewardTypeVal = QLineEdit()
        self.RewardTypeVal.setText(str(Reward_unit))
        
        RewardValLbl = QLabel("Unit Point ")
        self.RewardVal = QLineEdit()
        self.RewardVal.setText(str(Reward_point))
        self.RewardVal.setValidator(self.numeric_input_validator)
        
        save_button = QPushButton('SAVE')

        save_button.clicked.connect(lambda: self.Save_Reward(Reward_name))

        self.layout.addWidget(NameLbl,0,0)
        self.layout.addWidget(self.NameVal,0,1)
        self.layout.addWidget(RewardDescLbl,1,0)
        self.layout.addWidget(self.RewardDescVal,1,1)
        self.layout.addWidget(RewardTypeLbl,2,0)
        self.layout.addWidget(self.RewardTypeVal,2,1)
        self.layout.addWidget(RewardValLbl,3,0)
        self.layout.addWidget(self.RewardVal,3,1)

        self.layout.addWidget(save_button,4,1)

        self.setLayout(self.layout)

    def Save_Reward(self, Reward_name):
        newReward = self.NameVal.text()
        newDesc = self.RewardDescVal.text()
        newTpye = self.RewardTypeVal.text()
        newVal = self.RewardVal.text()

        if Reward_name == "":
            self.Reward_data.InsertReward(newReward, newDesc, newTpye, newVal)
        else:
            self.update_Reward.Reward_data(newReward, newDesc, newTpye, newVal, Reward_name)
        self.close()

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = RewardManagementWidget()
    window.show()
    sys.exit(pos_app.exec())
