import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 


class InitTableQuery():
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

    def initiate_item_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
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

    def initiate_item_type_table(self):
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

    def initiate_brand_table(self):
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

    def initiate_supplier_table(self):
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
    
    def initiate_sales_group_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SaleGrpId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            PromoId INTEGER DEFAULT 0,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (PromoId) REFERENCES Promo(PromoId)  -- Additional Promos
        );
        ''')
        self.conn.commit()
    
    def initiate_promo_table(self):
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

    def initiate_item_price_table(self):
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

    def initiate_customer_table(self):
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
    
    def initiate_stocks_table(self):
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

    def initiate_item_sold_table(self):
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

class AddItemQuery():
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
    
    def store_item_data(self, name, barcode, expire_dt):
        self.cursor.execute('''
        INSERT INTO Item (Name, Barcode, ExpireDt) VALUES (?,?,?)
        ''', (name, barcode, expire_dt))
        self.conn.commit()

    def store_item_type_data(self, name):
        self.cursor.execute('''
        INSERT INTO ItemType (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
        ''', (name,name))
        self.conn.commit()

    def store_brand_data(self, name):
        self.cursor.execute('''
        INSERT INTO Brand (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
        ''', (name,name))
        self.conn.commit()

    def store_supplier_data(self, name):
        self.cursor.execute('''
        INSERT INTO Supplier (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
        ''', (name,name))
        self.conn.commit()

    def store_sales_group_data(self, name):
        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
        ''', (name,name))
        self.conn.commit()

    # def store_promo_data(self):

    def store_item_price_data(self, cost, discount, sell_price):
        self.cursor.execute('''
        INSERT INTO ItemPrice (Cost, Discount, SellPrice) VALUES (?,?,?)
        ''', (cost, discount, sell_price))
        self.conn.commit()
    
    def store_customer_data(self):
        self.cursor.execute('''
        INSERT INTO Customer (CustId, CustName) VALUES (0,'unk')
        ''')
        self.conn.commit()

    def store_stocks_data(self):
        self.cursor.execute('''
        INSERT INTO Stocks (StockId, Description, OnHand, Available) VALUES (0,'unk', 0, 0)
        ''')
        self.conn.commit()

    # store ids
    def store_id_to_item(self, item_type_id, sales_group_id, supplier_id, name):
        self.cursor.execute('''
        UPDATE Item
        SET ItemTypeId = ?, SaleGrpId = ?, SupplierId = ?
        WHERE Name = ?
        ''', (item_type_id, sales_group_id, supplier_id, name))
        self.conn.commit()
        
    def store_id_to_item_price_data(self, item_id, item_price_id):
        self.cursor.execute('''
        UPDATE ItemPrice
        SET ItemId = ?
        WHERE ItemPriceId = ?
        ''', (item_id, item_price_id))
        self.conn.commit()

        
    # retrieve table ids
    def retrieve_item_id(self, name):
        self.cursor.execute('''
        SELECT ItemId FROM Item WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Assuming the first column is ItemId
        else:
            return None

    def retrieve_item_type_id(self, name):
        self.cursor.execute('''
        SELECT ItemTypeId FROM ItemType WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_brand_id(self, name):
        self.cursor.execute('''
        SELECT BrandId FROM Brand WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_supplier_id(self, name):
        self.cursor.execute('''
        SELECT SupplierId FROM Supplier WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_sales_group_id(self, name):
        self.cursor.execute('''
        SELECT SaleGrpId FROM SalesGroup WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_item_price_id(self, cost, discount, sell_price):
        self.cursor.execute('''
        SELECT ItemPriceId FROM ItemPrice WHERE Cost = ? AND Discount = ? AND SellPrice = ?
        ''', (cost, discount, sell_price))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_customer_id(self, name):
        self.cursor.execute('''
        SELECT CustomerId FROM Customer WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_promo_id(self, name):
        self.cursor.execute('''
        SELECT PromoId FROM Promo WHERE Name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_stocks_id(self, item_id):
        self.cursor.execute('''
        SELECT StocksId FROM Stocks WHERE ItemId = ?
        ''', (item_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def retrieve_item_sold_id(self, item_price_id, cust_id, stock_id, user_id):
        self.cursor.execute('''
        SELECT ItemSoldId FROM ItemSold WHERE ItemPriceId = ? AND CustId = ? AND StockId = ? AND UserId = ?
        ''', (item_price_id, cust_id, stock_id, user_id))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

class EditItemQuery():
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
 
    

class ListItemQuery():
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

    # def retrieve_item_name_data(self):
    #     self.cursor.execute('SELECT Name FROM Item')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_barcode_data(self):
    #     self.cursor.execute('SELECT Barcode FROM Item')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_expire_dt_data(self):
    #     self.cursor.execute('SELECT ExpireDt FROM Item')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_item_type_data(self):
    #     self.cursor.execute('SELECT Name FROM ItemType')
    #     result = self.cursor.fetchall()
    #     return result
        
    # def retrieve_brand_data(self):
    #     self.cursor.execute('SELECT Name FROM Brand')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_supplier_data(self):
    #     self.cursor.execute('SELECT Name FROM Supplier')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_sales_group_data(self):
    #     self.cursor.execute('SELECT Name FROM SalesGroup')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_cost_data(self):
    #     self.cursor.execute('SELECT Cost FROM ItemPrice')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_discount_data(self):
    #     self.cursor.execute('SELECT Discount FROM ItemPrice')
    #     result = self.cursor.fetchall()
    #     return result

    # def retrieve_sell_price_data(self):
    #     self.cursor.execute('SELECT SellPrice FROM ItemPrice')
    #     result = self.cursor.fetchall()
    #     return result

    def retrieve_item_data(self):
        self.cursor.execute('''
        SELECT 
            Item.Name, Item.Barcode, Item.ExpireDt, ItemType.Name, Brand.Name, 
            SalesGroup.Name, Supplier.Name, ItemPrice.Cost, ItemPrice.Discount, ItemPrice.SellPrice
        FROM 
            Item
            LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
            LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
            LEFT JOIN SalesGroup ON Item.SaleGrpId = SalesGroup.SaleGrpId
            LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN ItemPrice ON Item.ItemId = ItemPrice.ItemId
        ''')

        item_data = self.cursor.fetchall()

        return item_data

class SalesDropQuery():
    def __init__(self):
        super().__init__()

        # connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect('SALES.db')
        self.cursor = self.conn.cursor()

    def drop_item_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS Item;
        ''')
        self.conn.commit()

    def drop_item_type_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS ItemType;
        ''')
        self.conn.commit()

    def drop_brand_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS Brand;
        ''')
        self.conn.commit()

    def drop_sales_group_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS SalesGroup;
        ''')
        self.conn.commit()

    def drop_supplier_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS Supplier;
        ''')
        self.conn.commit()

    # (runs every Nth day of the month on ItemPrice ,  If near expiring Item(ExpireDt) - Today < N days then update ItemPrice(PromoId))
    def drop_promo_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS Promo;
        ''')
        self.conn.commit()

    def drop_item_price_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS ItemPrice;
        ''')
        self.conn.commit()

    def drop_customer_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS Customer;
        ''')
        self.conn.commit()

    def drop_stocks_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS Stocks;
        ''')
        self.conn.commit()

    def drop_item_sold_table(self):
        self.cursor.execute('''
        DROP TABLE IF EXISTS ItemSold;
        ''')
        self.conn.commit()
        
