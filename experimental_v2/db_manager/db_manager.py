import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

class CreateDatabaseTable():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # creates folder for the db file
        self.db_folder_path = 'sales/'
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()
    
    def create_database_table(self):
        # create table for item
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Barcode TEXT,
            ItemTypeId INTEGER DEFAULT 0,
            SalesGroupId INTEGER DEFAULT 0,
            SupplierId INTEGER DEFAULT 0,
            ExpireDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemTypeId) REFERENCES ItemType(ItemTypeId),
            FOREIGN KEY (SalesGroupId) REFERENCES SalesGroup(SalesGroupId),
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
        );
        ''')
        self.conn.commit()

        # create table for item type
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

        #create table for brand
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

        # create table for sales group
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()

        # create table for supplier
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()

        # create table for item price
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

        # create table for promo
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

        # create table for customer
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

        # create table for stocks
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

        # create table for item sold
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
        

class AddData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # creates folder for the db file
        self.db_folder_path = 'sales/'
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()
    
    def add_item_data(self, item_name, barcode, expire_dt, item_type, brand, sales_group, supplier, cost, discount, sell_price, effective_dt):
        # insert item data
        self.cursor.execute('''
        INSERT INTO Item (Name, Barcode, ExpireDt) VALUES (?,?,?)
        ''', (item_name, barcode, expire_dt))
        self.conn.commit()

        # insert item type data
        self.cursor.execute('''
        INSERT INTO ItemType (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
        ''', (item_type,item_type))
        self.conn.commit()

        # insert brand data
        self.cursor.execute('''
        INSERT INTO Brand (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
        ''', (brand,brand))
        self.conn.commit()

        # insert sales group data
        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
        ''', (sales_group,sales_group))
        self.conn.commit()

        # insert supplier data
        self.cursor.execute('''
        INSERT INTO Supplier (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
        ''', (supplier,supplier))
        self.conn.commit()

        # insert item price data
        self.cursor.execute('''
        INSERT INTO ItemPrice (Cost, Discount, SellPrice, EffectiveDt) VALUES (?,?,?,?)
        ''', (cost, discount, sell_price, effective_dt))
        self.conn.commit()

        self.close()
        
class RetrieveData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # creates folder for the db file
        self.db_folder_path = 'sales/'
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()
 
    def retrieve_item_id(self, item_name, barcode, expire_dt):
        self.cursor.execute('''
        SELECT ItemId FROM Item WHERE Name = ? AND Barcode = ? AND ExpireDt = ?
        ''', (item_name, barcode, expire_dt))

        item_id = self.cursor.fetchone()
        if item_id:
            return item_id[0]
        else:
            return None
        
    def retrieve_item_type_id(self, item_type):
        self.cursor.execute('''
        SELECT ItemTypeId FROM ItemType WHERE Name = ?
        ''', (item_type,))

        item_type_id = self.cursor.fetchone()
        if item_type_id:
            return item_type_id[0]
        else:
            return None

    def retrieve_brand_id(self, brand):
        self.cursor.execute('''
        SELECT BrandId FROM Brand WHERE Name = ?
        ''', (brand,))

        brand_id = self.cursor.fetchone()
        if brand_id:
            return brand_id[0]
        else:
            return None
        
    def retrieve_sales_group_id(self, sales_group):
        self.cursor.execute('''
        SELECT SalesGroupId FROM SalesGroup WHERE Name = ?
        ''', (sales_group,))

        sales_group_id = self.cursor.fetchone()
        if sales_group_id:
            return sales_group_id[0]
        else:
            return None
        
    def retrieve_supplier_id(self, supplier):
        self.cursor.execute('''
        SELECT SupplierId FROM Supplier WHERE Name = ?
        ''', (supplier,))

        supplier_id = self.cursor.fetchone()
        if supplier_id:
            return supplier_id[0]
        else:
            return None
        
    def retrieve_item_price_id(self, cost, discount, sell_price, effective_dt):
        self.cursor.execute('''
        SELECT ItemPriceId FROM ItemPrice WHERE Cost = ? AND Discount = ? AND SellPrice = ? AND EffectiveDt = ?
        ''', (cost, discount, sell_price, effective_dt))

        item_price_id = self.cursor.fetchone()
        if item_price_id:
            return item_price_id[0]
        else:
            return None
        
class UpdateData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # creates folder for the db file
        self.db_folder_path = 'sales/'
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()

    def update_table(self, item_id, item_type_id, sales_group_id, supplier_id, item_name, barcode, expire_dt, cost, discount, sell_price, effective_dt):
        self.cursor.execute('''
        UPDATE Item
        SET ItemTypeId = ?, SalesGroupId = ?, SupplierId = ?
        WHERE ItemId = ? AND Name = ? AND Barcode = ? AND ExpireDt = ?
        ''', (item_id, item_type_id, sales_group_id, supplier_id, item_name, barcode, expire_dt))

        self.cursor.execute('''
        UPDATE ItemPrice
        SET ItemId = ?
        WHERE ItemPriceId = ? AND Cost = ? AND Discount = ? AND SellPrice = ? AND EffectiveDt = ?
        ''', (item_id, item_type_id, cost, discount, sell_price, effective_dt))

        self.conn.close()
