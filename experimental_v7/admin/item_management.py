import sqlite3
import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database_table_setup import *
from utils.item_management_sql import *

class AddItemWindow(QDialog):
    data_saved = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')

        self.callSQLUtils()
        self.createLayout()
    
    def setInputValidator(self):
        self.item_price_input_validator = QDoubleValidator()
        self.item_price_input_validator.setDecimals(2)  # Set the number of decimal places
        self.item_price_input_validator.setRange(0.00, 999999.99) # Set the number of decimal places
        self.item_price_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.item_price_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

        self.stock_input_validator = QDoubleValidator()
        self.stock_input_validator.setDecimals(0)  # Set the number of decimal places
        self.stock_input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.stock_input_validator.setLocale(QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)) 

    def saveItem(self, raw_input):
        # convert input
        converted_barcode = str(raw_input[0].text())
        converted_item_name = str(raw_input[1].currentText())
        converted_expire_dt = raw_input[2].date().toString(Qt.DateFormat.ISODate)
        converted_item_type = str(raw_input[3].currentText())
        converted_brand = str(raw_input[4].currentText())
        converted_sales_group = str(raw_input[5].currentText())
        converted_supplier = str(raw_input[6].currentText())
        converted_cost = '{:.2f}'.format(float(raw_input[7].text()))
        converted_discount = '{:.2f}'.format(float(raw_input[8].text()))
        converted_sell_price = '{:.2f}'.format(float(raw_input[9].text()))
        converted_effective_dt = raw_input[10].date().toString(Qt.DateFormat.ISODate)
        converted_on_hand_stock = int(raw_input[14].text())
        converted_available_stock = int(raw_input[15].text())

        self.manage_item.insertItemTypeData(converted_item_type)
        self.manage_item.insertBrandData(converted_brand)
        self.manage_item.insertSalesGroupData(converted_sales_group)
        self.manage_item.insertSupplierData(converted_supplier)

        print('STEP A -- DONE')

        converted_item_type_id = self.manage_item.selectItemTypeId(converted_item_type)
        converted_brand_id = self.manage_item.selectBrandId(converted_brand)
        converted_sales_group_id = self.manage_item.selectSalesGroupId(converted_sales_group)
        converted_supplier_id = self.manage_item.selectSupplierId(converted_supplier)

        self.manage_item.insertItemData(converted_barcode, converted_item_name, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

        print('STEP B -- DONE')

        converted_item_id = self.manage_item.selectItemId(converted_barcode, converted_item_name, converted_expire_dt, converted_item_type_id, converted_brand_id, converted_sales_group_id, converted_supplier_id)

        self.manage_item.insertItemPriceData(converted_item_id, converted_cost, converted_discount, converted_sell_price, converted_effective_dt)

        print('STEP C -- DONE')

        self.data_saved.emit()

        print('NEW ITEM ADDED!')

        self.accept()

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()

    def setWidgetsAttributes(self):
        self.setInputValidator()

        self.item_name.setEditable(True)
        self.item_type.setEditable(True)
        self.brand.setEditable(True)
        self.supplier.setEditable(True)
        
        self.sales_group.addItem('Retail')
        self.sales_group.addItem('Wholesale')

        self.barcode.setPlaceholderText('Barcode')
        self.cost.setPlaceholderText('Cost')
        self.discount.setPlaceholderText('Discount')
        self.sell_price.setPlaceholderText('Sell price')

        self.cost.setValidator(self.item_price_input_validator)     
        self.discount.setValidator(self.item_price_input_validator)  
        self.sell_price.setValidator(self.item_price_input_validator)

        self.expire_dt.setMinimumDate(QDate.currentDate())
        self.effective_dt.setMinimumDate(QDate.currentDate())

        self.expire_dt.setCalendarPopup(True)
        self.effective_dt.setCalendarPopup(True)

        self.inventory_track_prompt.setText('Track inventory for this item?')
        self.track_y.setText('Yes')
        self.track_n.setText('No')
        self.track_n.setChecked(True)
        self.on_hand_stock.setPlaceholderText('On hand stock')
        self.on_hand_stock.setValidator(self.stock_input_validator)
        self.available_stock.setPlaceholderText('Available stock')
        self.available_stock.setValidator(self.stock_input_validator)

        self.save_button.setText('SAVE')
        self.save_button.clicked.connect(lambda: self.saveItem(self.raw_input))

    def createLayout(self):
        self.layout = QGridLayout()

        self.item_name = QComboBox()
        self.item_type = QComboBox()
        self.brand = QComboBox()
        self.sales_group = QComboBox()
        self.supplier = QComboBox()

        self.barcode = QLineEdit()
        self.cost = QLineEdit()
        self.discount = QLineEdit()
        self.sell_price = QLineEdit()
        self.on_hand_stock = QLineEdit()
        self.available_stock = QLineEdit()

        self.expire_dt = QDateEdit()
        self.effective_dt = QDateEdit()

        self.inventory_track_prompt = QLabel() 

        self.track_y = QRadioButton() 
        self.track_n = QRadioButton()

        self.save_button = QPushButton()
        
        self.setWidgetsAttributes()

        self.layout.addWidget(self.barcode, 0, 0) # -- barcode (widget[0])
        self.layout.addWidget(self.item_name, 1, 0) # -- item_name (widget[1])
        self.layout.addWidget(self.expire_dt, 2, 0) # -- expire_dt (widget[2])
        self.layout.addWidget(self.item_type, 3, 0) # -- item_type (widget[3])
        self.layout.addWidget(self.brand, 4, 0) # -- brand (widget[4])
        self.layout.addWidget(self.sales_group, 5, 0) # -- sales_group (widget[5])
        self.layout.addWidget(self.supplier, 6, 0) # -- supplier (widget[6])
        self.layout.addWidget(self.cost, 7, 0) # -- cost (widget[7])
        self.layout.addWidget(self.discount, 8, 0) # -- discount (widget[8])
        self.layout.addWidget(self.sell_price, 9, 0) # -- sell_price (widget[9])
        self.layout.addWidget(self.effective_dt, 10, 0) # -- effective_dt (widget[10])
        self.layout.addWidget(self.inventory_track_prompt, 11, 0) # -- inventory_track_prompt (widget[11]) x
        self.layout.addWidget(self.track_y, 12, 0) # -- track_y (widget[12]) x
        self.layout.addWidget(self.track_n, 13, 0) # -- track_n (widget[13]) x
        self.layout.addWidget(self.on_hand_stock, 14, 0) # -- on_hand_stock (widget[14])
        self.layout.addWidget(self.available_stock, 15, 0) # -- available_stock (widget[15])
        self.layout.addWidget(self.save_button, 16, 0) # -- save_button (widget[16]) x

        self.setLayout(self.layout)


class EditItemWindow(QDialog):

    
class ItemListTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.callSQLUtils()
        self.setAttributes()

    # def displayFilteredItemList(self, text_filter):
    #     all_item_data = self.manage_item.selectAllItemData(text_filter)

    #     self.setRowCount(50)

    #     for row_index, row_value in enumerate(all_item_data):
    #         for col_index, col_value in enumerate(row_value):
    #             self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
    #         self.edit_button = QPushButton()
    #         self.edit_button.setText('EDIT')
    #         self.setCellWidget(row_index, 0, self.edit_button)


    def displayItemList(self, text):
        all_item_data = self.manage_item.selectAllItemData(text)

        self.setRowCount(50)

        for row_index, row_value in enumerate(all_item_data):
            for col_index, col_value in enumerate(row_value):
                self.setItem(row_index, col_index + 1, QTableWidgetItem(str(col_value)))
            
            self.edit_button = QPushButton()
            self.edit_button.setText('EDIT')
            self.setCellWidget(row_index, 0, self.edit_button)

    def callSQLUtils(self):
        self.manage_item = ItemManagementSQL()

    def setAttributes(self):
        self.setColumnCount(12) # counts starting from 1 to n
        self.setHorizontalHeaderLabels(['','Barcode','Item name','Expire date','Item type','Brand','Sales group','Supplier','Cost','Discount','Sell price','Effective date'])
        
        self.displayItemList('')

class ItemManagement(QGroupBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Add Item')
        
        self.callSQLUtils()
        self.createLayout()

    def setWidgetsAttributes(self):
        self.filter_text.setPlaceholderText('Filter item by...')
        self.add_button.setText('ADD')
        self.add_button.clicked.connect(self.openAddItemWindow)

    def openAddItemWindow(self):
        add_item_window = AddItemWindow()
        add_item_window.data_saved.connect(lambda: self.item_list.displayItemList(''))
        add_item_window.exec()

    def callSQLUtils(self):
        self.database_table_setup = DatabaseTableSetup()

    def createLayout(self):
        self.database_table_setup.createDatabaseTable()

        self.layout = QGridLayout()

        self.filter_text = QLineEdit()
        self.add_button = QPushButton()
        self.item_list = ItemListTable()

        self.setWidgetsAttributes()

        self.layout.addWidget(self.filter_text,0,0)
        self.layout.addWidget(self.add_button,0,1)
        self.layout.addWidget(self.item_list,1,0,1,2)

        self.setLayout(self.layout)

if __name__ == ('__main__'):
    pos_app = QApplication(sys.argv)
    window = ItemManagement()
    window.show()
    sys.exit(pos_app.exec())




