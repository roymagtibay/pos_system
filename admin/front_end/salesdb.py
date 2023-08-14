import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

class SalesDBFunctions():
    def __init__(self, db_file = 'SALES.db'):

        # creates sqlite calendar db
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

# Item ---------------------------------------------------------------------------------------------------
    def create_item_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemName TEXT,
            Barcode TEXT,
            ItemTypeId INTEGER DEFAULT 0,
            SaleGrpId INTEGER DEFAULT 0,
            SupplierId INTEGER DEFAULT 0,
            ExpireDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemTypeId) REFERENCES ItemType(ItemTypeId),
            FOREIGN KEY (SaleGrpId) REFERENCES SalesGroup(SaleGrpId),
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
        );
        ''')
        self.conn.commit()

        self.conn.close()

    def insert_item_table(self, item_name, barcode, expiry_date):
        self.cursor.execute('''
        INSERT INTO Item (ItemName, Barcode, ExpireDt)  values (?,?,?)
        ''', (item_name, barcode, expiry_date))
        self.conn.commit()

        self.conn.close()

    def update_item_table(self, item_name, barcode, expiry_date, item_id):
        self.cursor.execute('''
        UPDATE Item
        SET
            ItemName = ?,
            Barcode = ?,
            ExpireDt = ?
        WHERE
            ItemId = ?
        ''', (item_name, barcode, expiry_date, item_id))
        self.conn.commit()

        self.conn.close()

# ItemType ---------------------------------------------------------------------------------------------------
    def create_item_type_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ItemType (
            ItemTypeId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()

        self.conn.close()
        
    def insert_item_type_table(self, item_type):
        self.cursor.execute('''
        INSERT INTO ItemType (Name)  values (?)
        ''', (item_type,))
        self.conn.commit()

        self.conn.close()

    def update_item_type_table(self, item_type, item_type_id):
        self.cursor.execute('''
        UPDATE ItemType
        SET
            Name = ?
        WHERE
            ItemTypeId = ?
        ''', (item_type, item_type_id))
        self.conn.commit()

        self.conn.close()


# Brand ---------------------------------------------------------------------------------------------------
    def create_item_brand_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Brand (
            BrandId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()

        self.conn.close()

    def insert_item_brand_table(self, brand):
        self.cursor.execute('''
        INSERT INTO Brand (Name)  values (?)
        ''', (brand,))
        self.conn.commit()

        self.conn.close()   

    def update_item_brand_table(self, brand, brand_id):
        self.cursor.execute('''
        UPDATE Brand
        SET
            Name = ?
        WHERE
            BrandId = ?
        ''', (brand, brand_id))
        self.conn.commit()

        self.conn.close()


# SalesGroup ---------------------------------------------------------------------------------------------------
    def create_sales_group_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SaleGrpId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        self.conn.close()

    def insert_sales_group_table(self, sales_group):
        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)  values (?)
        ''', (sales_group,))
        self.conn.commit()

        self.conn.close()

    def update_sales_group_table(self, sales_group, sales_group_id):
        self.cursor.execute('''
        UPDATE SalesGroup
        SET
            Name = ?
        WHERE
            SaleGrpId = ?
        ''', (sales_group, sales_group_id))
        self.conn.commit()

        self.conn.close()


# Supplier ---------------------------------------------------------------------------------------------------
    def create_supplier_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        self.conn.close()

    def insert_supplier_table(self, supplier):
        self.cursor.execute('''
        INSERT INTO Supplier (Name)  values (?)
        ''', (supplier,))
        self.conn.commit()

        self.conn.close()
 
    def update_supplier_table(self, supplier, supplier_id):
        self.cursor.execute('''
        UPDATE Supplier
        SET
            Name = ?
        WHERE
            SupplierId = ?
        ''', (supplier, supplier_id))
        self.conn.commit()

        self.conn.close()


# ItemPrice --------------------------------------------------------------------------------------------------- 
    def create_item_price_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ItemPrice (
            ItemPriceId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemId INTEGER DEFAULT 0,
            EffectiveDt DATETIME,
            PromoId INTEGER DEFAULT 0,
            Cost DECIMAL(15, 2),
            Discount DECIMAL(15, 2),
            SellPrice DECIMAL(15, 2),
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId),
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)
        );
        ''')
        self.conn.commit()

        self.conn.close()

    def insert_item_price_table(self, cost, discount, sell_price, effective_date):
        self.cursor.execute('''
        INSERT INTO ItemPrice (Cost, Discount, SellPrice, EffectiveDt)  values (?,?,?,?)
        ''', (cost, discount, sell_price, effective_date))
        self.conn.commit()

        self.conn.close()

    def update_item_price_table(self, cost, discount, sell_price, effective_date, item_price_id):
        self.cursor.execute('''
        UPDATE ItemPrice
        SET
            Cost = ?,
            Discount = ?,
            SellPrice = ?,
            EffectiveDt = ?
        WHERE
            ItemPriceId = ?
        ''', (cost, discount, sell_price, effective_date, item_price_id))
        self.conn.commit()

        self.conn.close()




    def get_item_id(self, item_name, barcode, expiry_date):
            self.cursor.execute('SELECT ItemId FROM Item WHERE ItemName = ? AND Barcode = ? AND ExpireDt = ?', (item_name, barcode, expiry_date))
            self.conn.commit()

            self.conn.close()
    
    def get_item_type_id(self, item_type):
            self.cursor.execute('SELECT ItemTypeId FROM ItemType WHERE Name = ?', (item_type,))
            self.conn.commit()

            self.conn.close()
    
    def get_brand_id(self, brand):
            self.cursor.execute('SELECT BrandId FROM Brand WHERE Name = ?', (brand,))
            self.conn.commit()

            self.conn.close()

    def get_supplier_id(self, supplier):
            self.cursor.execute('SELECT SupplierId FROM Supplier WHERE Name = ?', (supplier,))
            self.conn.commit()

            self.conn.close()

    def get_sales_group_id(self, sales_group):
            self.cursor.execute('SELECT SaleGrpId FROM SalesGroup WHERE Name = ?', (sales_group,))
            self.conn.commit()

            self.conn.close()
    
    def get_item_price_id(self, cost, discount, sell_price, effective_date):
            self.cursor.execute('SELECT ItemPriceId FROM ItemPrice WHERE Cost = ? AND Discount = ? AND SellPrice = ? AND EffectiveDt = ?', ( cost, discount, sell_price, effective_date))
            self.conn.commit()

            self.conn.close()
# Promo ---------------------------------------------------------------------------------------------------  (runs every Nth day of the month on ItemPrice ,  If near expiring Item(ExpireDt) - Today < N days then update ItemPrice(PromoId))
    def create_promo_table(self, promo):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Promo (
            PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoTyp TEXT,
            Description TEXT,
            DaysToExp INTEGER,
            LessPerc INTEGER,
            StartDt DATETIME,
            EndDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        self.conn.close()

        self.cursor.execute('''
        INSERT INTO Promo (Name)  values (?)
        ''', (promo,))
        self.conn.commit()

        self.conn.close()
    
# Customer --------------------------------------------------------------------------------------------------- 
    def create_customer_table(self, customer_name, address, phone, customer_type, status):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            CustId INTEGER PRIMARY KEY AUTOINCREMENT,
            CustName TEXT,
            Address TEXT,
            Phone TEXT,
            Type TEXT,
            Status TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        self.conn.close()

        self.cursor.execute('''
        INSERT INTO Customer (CustName, Address, Phone, Type, Status)  values (?,?,?,?,?)
        ''', (customer_name, address, phone, customer_type, status))
        self.conn.commit()

        self.conn.close()
    
# Stocks --------------------------------------------------------------------------------------------------- 
    def create_stocks_table(self, description, on_hand, available):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Stocks (
            StockId INTEGER PRIMARY KEY AUTOINCREMENT,
            SupplierId INTEGER DEFAULT 0,
            ItemId INTEGER DEFAULT 0,
            Description TEXT,
            OnHand INTEGER,
            Available INTEGER,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId),
            FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
        );
        ''')
        self.conn.commit()

        self.conn.close()

        self.cursor.execute('''
        INSERT INTO Stocks (Description, OnHand, Available)  values (?,?,?)
        ''', (description, on_hand, available))
        self.conn.commit()

        self.conn.close()
    
# ItemSold --------------------------------------------------------------------------------------------------- 
    def create_item_sold_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ItemSold (
            ItemSoldId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemPriceId INTEGER DEFAULT 0,
            CustId INTEGER DEFAULT 0,
            StockId INTEGER DEFAULT 0,
            UserId INTEGER DEFAULT 0,
            Quantity INTEGER,
            TotalAmount DECIMAL(15, 2),
            Void BIT DEFAULT 0, 
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ItemPriceId) REFERENCES ItemPrice(ItemPriceId),
            FOREIGN KEY (CustId) REFERENCES Customer(CustId),
            FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
        );
        ''')
        self.conn.commit()

        self.conn.close()
