import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

class InitDatabaseTable():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def database_table(self):
        # ItemType
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

        # Brand
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

        # SalesGroup
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS SalesGroup (
            SalesGroupId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # Supplier
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        self.conn.commit()

        # Item
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            ItemId INTEGER PRIMARY KEY AUTOINCREMENT,
            ItemName TEXT,
            Barcode TEXT,
            ItemTypeId INTEGER DEFAULT 0,
            BrandId INTEGER DEFAULT 0,
            SalesGroupId INTEGER DEFAULT 0,
            SupplierId INTEGER DEFAULT 0,
            ExpireDt DATETIME,
            UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (ItemTypeId) REFERENCES ItemType(ItemTypeId),
            FOREIGN KEY (BrandId) REFERENCES Brand(BrandId),
            FOREIGN KEY (SalesGroupId) REFERENCES SalesGroup(SalesGroupId),
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId)
        );
        ''')
        self.conn.commit()

        # ItemPrice
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

# queries for adding item/s
class StoreData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def item_type_data(self, item_type):
        self.cursor.execute('''
        INSERT INTO ItemType (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
        ''', (item_type, item_type))
        self.conn.commit()

    def brand_data(self, brand):
        self.cursor.execute('''
        INSERT INTO Brand (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
        ''', (brand, brand))
        self.conn.commit()
    
    def sales_group_data(self, sales_group):
        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
        ''', (sales_group, sales_group))
        self.conn.commit()

    def supplier_data(self, supplier):
        self.cursor.execute('''
        INSERT INTO Supplier (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
        ''', (supplier, supplier))
        self.conn.commit()

    def item_data(self, item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        INSERT INTO Item (ItemName, Barcode, ExpireDt, ItemTypeId, BrandId, SalesGroupId, SupplierId)
        SELECT ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Item
            INNER JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
            INNER JOIN Brand ON Item.BrandId = Brand.BrandId
            INNER JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
            INNER JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
        WHERE
            Item.ItemName = ? AND
            Item.Barcode = ? AND
            Item.ExpireDt = ? AND
            Item.ItemTypeId = ? AND
            Item.BrandId = ? AND
            Item.SupplierId = ? AND
            Item.SalesGroupId = ?
        )''', (item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id,
              item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        self.conn.commit()

    def item_price_data(self, item_id, cost, discount, sell_price, effective_dt):
        self.cursor.execute('''
        INSERT INTO ItemPrice (ItemId, Cost, Discount, SellPrice, EffectiveDt)
        SELECT ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
        SELECT 1 FROM ItemPrice
        WHERE 
            ItemId = ? AND
            Cost = ? AND
            Discount = ? AND
            SellPrice = ? AND
            EffectiveDt = ?
        )''', (item_id, cost, discount, sell_price, effective_dt,
              item_id, cost, discount, sell_price, effective_dt))
        self.conn.commit()

class RetrieveId():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def item_type_id(self, item_type):
        self.cursor.execute('''
        SELECT ItemTypeId FROM ItemType
        WHERE Name = ?
        ''', (item_type,))

        item_type_id = self.cursor.fetchone()

        return item_type_id[0]

    def brand_id(self, brand):
        self.cursor.execute('''
        SELECT BrandId FROM Brand
        WHERE Name = ?
        ''', (brand,))

        brand_id = self.cursor.fetchone()

        return brand_id[0]

    def sales_group_id(self, sales_group):
        self.cursor.execute('''
        SELECT SalesGroupId FROM SalesGroup
        WHERE Name = ?
        ''', (sales_group,))

        sales_group_id = self.cursor.fetchone()

        return sales_group_id[0]

    def supplier_id(self, supplier):
        self.cursor.execute('''
        SELECT SupplierId FROM Supplier
        WHERE Name = ?
        ''', (supplier,))

        supplier_id = self.cursor.fetchone()

        return supplier_id[0]

    def item_id(self, item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        SELECT ItemId FROM Item
        WHERE ItemName = ? AND Barcode = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
        ''', (item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))

        item_id = self.cursor.fetchone()

        return item_id[0]

    def item_price_id(self, item_id, cost, discount, sell_price, effective_dt):
        self.cursor.execute('''
        SELECT ItemPriceId FROM ItemPrice
        WHERE ItemId = ? AND Cost = ? AND Discount = ? AND SellPrice = ? AND EffectiveDt = ?
        ''', (item_id, cost, discount, sell_price, effective_dt))

        item_price_id = self.cursor.fetchone()

        return item_price_id[0]

        # self.cursor.execute('''
        # CREATE TABLE IF NOT EXISTS Promo (
        #     PromoId INTEGER PRIMARY KEY AUTOINCREMENT,
        #     Name TEXT,
        #     PromoTyp TEXT,
        #     Description TEXT,
        #     DaysToExp INTEGER,
        #     LessPerc INTEGER,
        #     StartDt DATETIME,
        #     EndDt DATETIME,
        #     UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        # );
        # ''')
        # self.conn.commit()

        # self.cursor.execute('''
        # CREATE TABLE IF NOT EXISTS Customer (
        #     CustId INTEGER PRIMARY KEY AUTOINCREMENT,
        #     CustName TEXT,
        #     Address TEXT,
        #     Phone TEXT,
        #     Type TEXT,
        #     Status TEXT,
        #     UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP
        # );
        # ''')
        # self.conn.commit()

        # self.cursor.execute('''
        # CREATE TABLE IF NOT EXISTS Stocks (
        #     StockId INTEGER PRIMARY KEY AUTOINCREMENT,
        #     SupplierId INTEGER DEFAULT 0,
        #     ItemId INTEGER DEFAULT 0,
        #     Description TEXT,
        #     OnHand INTEGER,
        #     Available INTEGER,
        #     UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
        #     FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId),
        #     FOREIGN KEY (ItemId) REFERENCES Item(ItemId)
        # );
        # ''')
        # self.conn.commit()

        # self.cursor.execute('''
        # CREATE TABLE IF NOT EXISTS ItemSold (
        #     ItemSoldId INTEGER PRIMARY KEY AUTOINCREMENT,
        #     ItemPriceId INTEGER DEFAULT 0,
        #     CustId INTEGER DEFAULT 0,
        #     StockId INTEGER DEFAULT 0,
        #     UserId INTEGER DEFAULT 0,
        #     Quantity INTEGER,
        #     TotalAmount DECIMAL(15, 2),
        #     Void BIT DEFAULT 0, 
        #     UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
        #     FOREIGN KEY (ItemPriceId) REFERENCES ItemPrice(ItemPriceId),
        #     FOREIGN KEY (CustId) REFERENCES Customer(CustId),
        #     FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
        # );
        # ''')
        # self.conn.commit()

class ChangeData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def all_item_data(self, item_name, barcode, expire_dt, item_type, brand, sales_group, supplier, item_id, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        UPDATE Item
        SET ItemName = ?,
            Barcode = ?,
            ExpireDt = ?
        WHERE ItemId = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?;
        ''', (item_name, barcode, expire_dt, item_id, item_type_id, brand_id, sales_group_id, supplier_id))
        
        self.cursor.execute('''
        UPDATE ItemType
        SET Name = ?
        WHERE ItemTypeId = (SELECT ItemTypeId FROM Item WHERE ItemId = ?)
        ''', (item_type, item_id))
        
        self.cursor.execute('''
        UPDATE Brand
        SET Name = ?
        WHERE BrandId = (SELECT BrandId FROM Item WHERE ItemId = ?)
        ''', (brand, item_id))
        
        self.cursor.execute('''
        UPDATE SalesGroup
        SET Name = ?
        WHERE SalesGroupId = (SELECT SalesGroupId FROM Item WHERE ItemId = ?)
        ''', (sales_group, item_id))
        
        self.cursor.execute('''
        UPDATE Supplier
        SET Name = ?
        WHERE SupplierId = (SELECT SupplierId FROM Item WHERE ItemId = ?)
        ''', (supplier, item_id))

        self.conn.commit()

# queries for listing item/s
class RetrieveData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def all_item_data(self):
        self.cursor.execute('''
        SELECT
            COALESCE(Item.ItemName, 'unk'),
            COALESCE(Item.Barcode, 'unk'),
            COALESCE(Item.ExpireDt, 'unk'), 
            COALESCE(ItemType.Name, 'unk') AS ItemType, 
            COALESCE(Brand.Name, 'unk') AS Brand, 
            COALESCE(SalesGroup.Name, 'unk') AS SalesGroup, 
            COALESCE(Supplier.Name, 'unk') AS Supplier, 
            COALESCE(ItemPrice.Cost, 0.00) AS Cost, 
            COALESCE(ItemPrice.Discount, 0.00) AS Discount, 
            COALESCE(ItemPrice.SellPrice, 0.00) AS SellPrice,
            COALESCE(ItemPrice.EffectiveDt, 'unk') AS EffectiveDt,
            Item.ItemId,
            ItemType.ItemTypeId,
            Brand.BrandId,
            SalesGroup.SalesGroupId,
            Supplier.SupplierId
                            
        FROM ItemPrice
            LEFT JOIN Item
                ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN ItemType
                ON Item.ItemTypeId = ItemType.ItemTypeId
            LEFT JOIN Brand
                ON Item.BrandId = Brand.BrandId
            LEFT JOIN Supplier
                ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN SalesGroup
                ON Item.SalesGroupId = SalesGroup.SalesGroupId
        ''')
        
        all_data = self.cursor.fetchall()

        return all_data
    

