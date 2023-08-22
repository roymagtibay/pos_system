import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.user_management_sql import *

class UserManagementWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('User Management')
        self.create_table = CreateDatabaseTable()
        self.create_table.database_table()
        self.call_sql_utils()
        self.init_layout()

    # call sql queries 
    def call_sql_utils(self):
        self.user_crud = UserDataCRUD()

    def init_layout(self):
        layout_header = QVBoxLayout()

        self.Page_Title = QLabel("User Settings", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.Page_Title.setStyleSheet(''' font-size: 24px; color: "Blue" ''')

        layout_header.addWidget(self.Page_Title)
        layout_header.setSpacing(0)
        layout_header.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_widget.setLayout(layout_header)

        self.layout = QGridLayout()

        self.Usertypes = QComboBox(self)
        self.Usertypes.setStyleSheet(''' color: "blue";  ''')
        self.Usertypes.setEditable(False)
        self.Usertypes.addItem("All")
        self.Usertypes.addItem("Admin")
        self.Usertypes.addItem("Cashier")
        Usertypes = self.Usertypes

        self.add_user_button = QPushButton('ADD')

        #self.layout.addRow(QLabel(""))
        self.layout.addWidget(self.Usertypes,0,0) 
        self.layout.addWidget(self.add_user_button,0,1)

        self.user_list_table = UserListTable(self.Usertypes.currentText())
        self.layout.addWidget(self.user_list_table,1,0,1,2)

        self.Usertypes.currentIndexChanged.connect(self.populate_table)  # connects to user_crud functions every change of text

        self.add_user_button.clicked.connect(lambda: self.user_list_table.save_user_window("", "", ""))

        # Create the main layout and add the header and details layouts
        #self.main_layout = QVBoxLayout()
        #self.main_layout.addLayout(header_widget)
        #self.main_layout.addLayout(self.layout)

        self.setLayout(self.layout)

        self.setWindowTitle('Item Promo Management')

    def populate_table(self, data):
        filter_input = self.Usertypes.currentText()
        self.user_list_table.populate_UserList(filter_input)


class UserListTable(QTableWidget):
    data_saved = pyqtSignal()
    def __init__(self, filtertext):
        super().__init__()       
        self.call_sql_utils()
        self.init_layout(filtertext)

    def call_sql_utils(self):
        self.user_crud = UserDataCRUD()

    def init_layout(self,filtertext):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["","Name", "Level"])
        
        self.populate_UserList(filtertext)
    
    def populate_UserList(self,filtertext):
        selected_item = filtertext
        self.clearContents()

        if selected_item == "All":
            data = self.user_crud.select_alluser()
        elif selected_item == "Admin":
            data = self.user_crud.select_user('2')
        else:
            data = self.user_crud.select_user('1')    

        self.setRowCount(len(data))    

        for row_index, (user_name, user_level) in enumerate(data):
            self.setItem(row_index, 1, QTableWidgetItem(str(user_name)))
            self.setItem(row_index, 2, QTableWidgetItem(str(user_level)))
            self.edit_tem_button = QPushButton('EDIT')
            self.edit_tem_button.clicked.connect(lambda row_index=row_index, user_name=user_name, user_level=user_level : self.save_user_window(row_index, user_name, user_level))
            self.setCellWidget(row_index, 0, self.edit_tem_button)    

    def save_user_window(self, row_index, user_name, user_level):
        edit_item_dialog = SaveUserDialog(row_index, user_name, user_level)
        edit_item_dialog.exec()
        self.populate_UserList('All')

        self.data_saved.emit()

   

class SaveUserDialog(QDialog):
    data_saved = pyqtSignal()
    def __init__(self, row_index, user_name, user_level):
        super().__init__()
        self.newUser=""

        self.call_sql_utils()
        self.init_layout(row_index, user_name, user_level)

    def call_sql_utils(self):
        self.user_crud = UserDataCRUD()

    def init_layout(self, row_index, user_name, user_level):
        self.layout = QGridLayout()

        UsernameLbl = QLabel("Username ")

        self.UsernameVal = QLineEdit()
        self.UsernameVal.setText(str(user_name))
        if user_name == "":
            self.newUser="Y"

        UserPwdLbl = QLabel("Password ")
        self.UserPwdVal = QLineEdit()
        self.UserPwdVal.setPlaceholderText("<Please input password>")
        
        UserLvlLbl = QLabel("Access Level ")
        self.UserPLvlVal = QLineEdit()
        self.UserPLvlVal.setText(str(user_level))
        

        save_button = QPushButton('SAVE')

        save_button.clicked.connect(lambda: self.Save_User(user_name))

        self.layout.addWidget(UsernameLbl,0,0)
        self.layout.addWidget(self.UsernameVal,0,1)
        self.layout.addWidget(UserPwdLbl,1,0)
        self.layout.addWidget(self.UserPwdVal,1,1)
        self.layout.addWidget(UserLvlLbl,2,0)
        self.layout.addWidget(self.UserPLvlVal,2,1)

        self.layout.addWidget(save_button,3,1)

        self.setLayout(self.layout)

    def Save_User(self, user_name):
        newUser = self.UsernameVal.text()
        newPwd = self.UserPwdVal.text()
        newLvl = self.UserPLvlVal.text()

        if self.newUser == "Y":
            self.user_crud.create_user(newUser, newPwd, newLvl)
        else:    
            self.user_crud.update_user(user_name, newPwd, newLvl)

        self.close()

        



if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = UserManagementWidget()
    window.show()
    sys.exit(pos_app.exec())
