import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

# for storing item data
class InsertStockData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def stock_data(self, supplier_id, item_id, on_hand, available):
        self.cursor.execute('''
        INSERT INTO Stock (SupplierId, ItemId, OnHand, Available)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Stock
            INNER JOIN Item ON Stock.ItemId = Item.ItemId
            INNER JOIN Supplier ON Stock.SupplierId = Supplier.SupplierId
        WHERE
            Stock.SupplierId = ? AND
            Stock.ItemId = ? AND
            Stock.OnHand = ? AND
            Stock.Available = ?
        )''', (supplier_id, item_id, on_hand, available,
              supplier_id, item_id, on_hand, available))
        self.conn.commit()

# for retrieving ids
class SelectStockId():
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
        # CREATE TABLE IF NOT EXISTS Stock (
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
        #     FOREIGN KEY (StockId) REFERENCES Stock(StockId)
        # );
        # ''')
        # self.conn.commit()

# for editing items
class UpdateStockData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def stock_data(self, on_hand, available, supplier_id, item_id):
        self.cursor.execute('''
        UPDATE Stock
        SET OnHand = ?, Available = ?
        WHERE SupplierId = ? AND ItemId = ?
        ''', (on_hand, available, supplier_id, item_id))
        self.conn.commit()

# for listing data
class SelectStockData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def all_stock_data(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Supplier.Name, 'unk') AS Supplier,
            COALESCE(Item.ItemName, 'unk') AS ItemName, 
            Stock.OnHand,
            Stock.Available,
            Supplier.SupplierId,
            Item.ItemId     
        FROM ItemPrice
            LEFT JOIN Item
                ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN Supplier
                ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN Stock
                ON Stock.ItemId = Item.ItemId
        WHERE
            Stock.OnHand IS NOT NULL AND
            Stock.Available IS NOT NULL
        ''')
        
        all_data = self.cursor.fetchall()

        return all_data
    
    def filtered_stock_data(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Supplier.Name, 'unk') AS Supplier,
            COALESCE(Item.ItemName, 'unk') AS ItemName, 
            Stock.OnHand,
            Stock.Available  
        FROM ItemPrice
            LEFT JOIN Item
                ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN Supplier
                ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN Stock
                ON Stock.ItemId = Item.ItemId
        WHERE
            (Stock.OnHand IS NOT NULL AND Stock.Available IS NOT NULL) AND
            (Supplier.Name LIKE ? OR Item.ItemName LIKE ? OR Stock.OnHand LIKE ? OR Stock.Available LIKE ?)
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        stock = self.cursor.fetchall()

        return stock
