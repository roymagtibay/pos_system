import sys
from PyQt6.QtWidgets import QApplication
from promo_management import ManagePromo

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # these are the arguments to be passed to ManagePromo widget,  the values should be available from Item Add / ItemEdit / Process Sale  
    # values are just dummy data for testing purposes
    Item_Price_Id = "1"
    Item_Id = "1"
    Name = "Item 1" 
    Type = "Snacks" 
    Brand = "Regent" 
    Sales_Group = "Retail" 
    Supplier = "Cabral" 
    Expire_Date = "2023-12-31"
    Promo = "EXP"
    LessAmount = "-1.6"
    Cost = "10"
    SellPrice = "10.4"

    widget = ManagePromo(Item_Price_Id, Item_Id, Name, Type, Brand, Sales_Group, Supplier, Expire_Date, Cost, Promo, LessAmount, SellPrice)
    #widget = 
    widget.show()

    app.setStyleSheet("""
    QWidget {
        background-color: rgb(47,79,79);
        color: "white";
    }
    QPushButton {
        font-size: 16px;
        background-color: "darkgreen"
    }
    QLineEdit {
        background-color: "white";
        color: "black";
    }
    QLable {
        color: "white";
    }
    QComboBox {
        background-color: "white";
        color: "black";
    }
    """)
    
    sys.exit(app.exec())
