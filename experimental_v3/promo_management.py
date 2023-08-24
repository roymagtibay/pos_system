import sys
import sqlite3
from PyQt6.QtWidgets import QWidget, QLabel, QFormLayout, QLineEdit, QVBoxLayout, QComboBox, QPushButton, QDateEdit, QMessageBox
from PyQt6.QtCore import Qt, QDate
from db_manager import ItemPromo

class ManagePromo(QWidget):
    def __init__(self, Item_Price_Id, Item_Id, Name, Type_Id, Brand_Id, Sales_Group_Id, Supplier_Id, Expire_Date, Cost, Promo, LessAmount, SellPrice):
        super().__init__()

        self.ItemPromo = ItemPromo()

        self.setFixedSize(320, 650)  # Set window position and size

        self.ItemPromoLayout(Item_Price_Id, Item_Id, Name, Type_Id, Brand_Id, Sales_Group_Id, Supplier_Id, Expire_Date, Cost, Promo, LessAmount, SellPrice)
    
    def ItemPromoLayout(self, Item_Price_Id, ItemId, Name, Type, Brand, Sales_Group, Supplier, Expire_Date, Cost, Promo, LessAmount, SellPrice):

        layout_header = QVBoxLayout()

        self.Page_Title = QLabel("I T E M   P R O M O", alignment=Qt.AlignmentFlag.AlignHCenter)
        self.Page_Title.setStyleSheet(''' font-size: 24px; color: rgb(255,215,0) ''')

        layout_header.addWidget(self.Page_Title)
        layout_header.setSpacing(0)
        layout_header.setContentsMargins(0, 0, 0, 0)

        header_widget = QWidget()
        header_widget.setLayout(layout_header)
        
        header_widget.setFixedHeight(40)  # Adjust the height as needed
        header_widget.setStyleSheet(''' background-color: "black"; ''') 

        layout = QFormLayout()

        ItemId_column = QLabel("Item Id ")
        ItemId_column.setStyleSheet(''' font-size: 16px; ''')
        Name_column = QLabel("Name ")
        Name_column.setStyleSheet(''' font-size: 16px; ''')
        Type_column = QLabel("Type ")
        Type_column.setStyleSheet(''' font-size: 16px; ''')
        Brand_column = QLabel("Brand ")
        Brand_column.setStyleSheet(''' font-size: 16px; ''')
        Sales_Group_column = QLabel("Sales Group ")
        Sales_Group_column.setStyleSheet(''' font-size: 16px; ''')
        Supplier_column = QLabel("Supplier ")
        Supplier_column.setStyleSheet(''' font-size: 16px; ''')
        Expire_column = QLabel("Expire Date ")
        Expire_column.setStyleSheet(''' font-size: 16px; ''')
        PromoTag_column = QLabel("Promo Tag ")
        PromoTag_column.setStyleSheet(''' font-size: 16px; ''')
        Promo_Type_column = QLabel("Select Promo Type For Item ")
        Promo_Type_column.setStyleSheet(''' font-size: 16px; color: "gold"''')
        Discount_column = QLabel("% Discount ")
        Discount_column.setStyleSheet(''' font-size: 16px; ''')
        PromoStart_column = QLabel("Start Date ")
        PromoStart_column.setStyleSheet(''' color: "gold"; font-size: 16px; ''')
        PromoEnd_column = QLabel("End Date ")
        PromoEnd_column.setStyleSheet(''' color: "gold"; font-size: 16px; ''')


        Item_Id = QLineEdit(ItemId, self)
        Item_Id.setStyleSheet(''' font-size: 16px; ''')
        Item_Id.setReadOnly(True)
        Item_Id.setFixedSize(200,20)

        Name = QLineEdit(Name, self)
        Name.setStyleSheet(''' font-size: 16px; ''')
        Name.setReadOnly(True)
        Name.setFixedSize(200,20)

        Type = QLineEdit(Type, self)
        Type.setStyleSheet(''' font-size: 16px; ''')
        Type.setReadOnly(True)
        Type.setFixedSize(200,20)

        Brand = QLineEdit(Brand, self)
        Brand.setStyleSheet(''' font-size: 16px; ''')
        Brand.setReadOnly(True)
        Brand.setFixedSize(200,20)

        Sales_Group = QLineEdit(Sales_Group, self)
        Sales_Group.setStyleSheet(''' font-size: 16px; ''')
        Sales_Group.setReadOnly(True)
        Sales_Group.setFixedSize(200,20)

        Supplier = QLineEdit(Supplier, self)
        Supplier.setStyleSheet(''' font-size: 16px; ''')
        Supplier.setReadOnly(True)
        Supplier.setFixedSize(200,20)

        ExpireDt = QLineEdit(Expire_Date, self)
        ExpireDt.setStyleSheet(''' font-size: 16px; ''')
        ExpireDt.setReadOnly(True)
        ExpireDt.setFixedSize(200,20)

        PromoTag = QLineEdit(Promo, self)
        PromoTag.setStyleSheet(''' font-size: 16px; ''')
        PromoTag.setReadOnly(True)
        PromoTag.setFixedSize(200,20)

        self.promotype_combo = QComboBox(self)
        self.promotype_combo.setStyleSheet(''' color: "blue"; background-color: "yellow"; font-size: 16px; ''')
        self.promotype_combo.setEditable(False)
        self.promotype_combo.setFixedSize(200,20)
        self.getPromotype()

        self.PromoTypeIdx = self.promotype_combo.currentIndex()

        self.PromoName = QLineEdit(self)
        self.PromoName.setStyleSheet(''' font-size: 16px; ''')
        self.PromoName.setReadOnly(True)
        self.PromoName.setFixedSize(200,20)
        self.PromoName.setText(str(self.PromoDetails[self.PromoTypeIdx][2]))

        self.PromoId = QLineEdit(self)
        self.PromoId.setText(str(self.PromoDetails[self.PromoTypeIdx][0]))
        self.PromoId.setVisible(False)
        

        self.Discount = QLineEdit(self)
        self.Discount.setStyleSheet(''' font-size: 16px; ''')
        self.Discount.setReadOnly(True)
        self.Discount.setFixedSize(200,20)
        self.Discount.setText(str(self.PromoDetails[self.PromoTypeIdx][3]))

        PercDiscount = self.Discount.text()

        self.PromoStart = QDateEdit(self)
        self.PromoStart.setStyleSheet(''' color: "blue"; font-size: 16px; background-color: "white" ''')
        self.PromoStart.setCalendarPopup(True)
        self.PromoStart.setDate(QDate.currentDate())
        self.PromoStart.setFixedSize(200,20)
        self.PromoStart.setDisplayFormat("yyyy-MM-dd")
        self.PromoStart.dateChanged.connect(self.StartDatePicked)

        self.StartDate = QLineEdit(self)
        self.StartDate.setVisible(False)
        selected_date = self.PromoStart.date()
        self.StartDate.setText(selected_date.toString("yyyy-MM-dd")) 

        self.PromoEnd = QDateEdit(self)
        self.PromoEnd.setStyleSheet(''' color: "blue"; font-size: 16px; background-color: "white" ''')
        self.PromoEnd.setCalendarPopup(True)
        self.PromoEnd.setDate(QDate.currentDate())
        self.PromoEnd.setFixedSize(200,20)
        self.PromoEnd.setDisplayFormat("yyyy-MM-dd")
        self.PromoEnd.dateChanged.connect(self.EndDatePicked)

        self.EndDate = QLineEdit(self)
        self.EndDate.setVisible(False)
        selected_date = self.PromoEnd.date()
        self.EndDate.setText(selected_date.toString("yyyy-MM-dd")) 

        layout.addRow(QLabel(""))
        layout.addRow(ItemId_column,Item_Id)
        layout.addRow(Name_column,Name)
        layout.addRow(Type_column,Type)
        layout.addRow(Brand_column,Brand)
        layout.addRow(Sales_Group_column,Sales_Group)
        layout.addRow(Supplier_column,Supplier)
        layout.addRow(Expire_column,ExpireDt)
        layout.addRow(PromoTag_column,PromoTag)
        layout.addRow(QLabel(""))
        layout.addRow(Promo_Type_column)
        
        layout.addWidget(self.promotype_combo)
        layout.addWidget(self.PromoName)

        layout.addRow(Discount_column,self.Discount)
        
        layout.addRow(PromoStart_column,self.PromoStart)
        layout.addRow(PromoEnd_column,self.PromoEnd)

        self.promotype_combo.currentIndexChanged.connect(self.selection_changed)

        # Create the main layout and add the header and details layouts
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(header_widget)
        self.main_layout.addLayout(layout)

        self.setLayout(self.main_layout)

        self.setWindowTitle('Item Promo Management')

        layout.addRow(QLabel(""))
        layout.addRow(QLabel(""))

        self.save_button = QPushButton("Save", self)
        self.save_button.setFixedSize(150, 40)
        self.save_button.setStyleSheet(''' color: "black"; background-color: rgb(240,230,140); ''')
        
        layout.addRow(self.save_button)
        layout.setAlignment(self.save_button, Qt.AlignmentFlag.AlignHCenter)
        self.save_button.clicked.connect(lambda: self.InsertItemPromo(ItemId, Cost, LessAmount, SellPrice ))

        self.close_button = QPushButton("Close", self)
        self.close_button.setFixedSize(150, 40)
        self.close_button.setStyleSheet(''' color: "black"; background-color: rgb(240,230,140); ''')

        layout.addRow(self.close_button)
        layout.setAlignment(self.close_button, Qt.AlignmentFlag.AlignHCenter)
        self.close_button.clicked.connect(self.close_window)

    def StartDatePicked(self):
        selected_date = self.PromoStart.date()
        self.StartDate.setText(selected_date.toString("yyyy-MM-dd")) 

    def EndDatePicked(self):
        selected_date = self.PromoEnd.date()
        nextday = selected_date.addDays(+1)
        self.EndDate.setText(nextday.toString("yyyy-MM-dd")) 
        
    def InsertItemPromo(self, ItemId, Cost, LessAmount, SellPrice):
        Promo_Id = int(self.PromoId.text())
        PercDiscount = float(self.Discount.text())
        Promo_Date = self.StartDate.text()
        
        if Promo_Id == 0:
            NewSellPrice = float(SellPrice) + abs(float(LessAmount))
        else:
            NewSellPrice = float(SellPrice) - (float(SellPrice) * (float(PercDiscount)/100))

        self.ItemPromo.InsertItemPrice(ItemId, Promo_Date, Promo_Id, Cost, PercDiscount, NewSellPrice)

        if Promo_Id > 0:
            Promo_Date = self.EndDate.text()
            NewSellPrice = float(SellPrice)

            self.ItemPromo.InsertItemPrice(ItemId, Promo_Date, Promo_Id, Cost, PercDiscount, NewSellPrice)

        QMessageBox.information(self, "Success", "Item Promo saved successfully.")
        self.close()

    def selection_changed(self):
        self.PromoTypeIdx = self.promotype_combo.currentIndex()
        self.PromoId.setText(str(self.PromoDetails[self.PromoTypeIdx][0]))
        self.PromoName.setText(str(self.PromoDetails[self.PromoTypeIdx][2]))
        self.Discount.setText(str(self.PromoDetails[self.PromoTypeIdx][3]))

    def getPromotype(self):
        self.PromoDetails = self.ItemPromo.FetchPromoTypes()
        for PromoRow in self.PromoDetails:
            Promotype = PromoRow[1]
            self.promotype_combo.addItem(str(Promotype))

    def close_window(self):
        self.close()
