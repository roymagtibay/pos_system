import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

# for storing item data
class InsertItemData():
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

# for retrieving ids
class SelectItemId():
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

# for editing items
class UpdateItemData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def item_data(self, item_name, barcode, expire_dt, item_id, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        UPDATE Item
        SET ItemName = ?,
            Barcode = ?,
            ExpireDt = ?
        WHERE ItemId = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?;
        ''', (item_name, barcode, expire_dt, item_id, item_type_id, brand_id, sales_group_id, supplier_id))

        self.conn.commit()

# for listing data
class SelectItemData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def all_item_data(self, text):
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
        WHERE
            Item.ItemName LIKE ? OR
            Item.Barcode LIKE ? OR
            ItemType.Name LIKE ? OR
            Brand.Name LIKE ? OR
            SalesGroup.Name LIKE ? OR
            Supplier.Name LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        all_data = self.cursor.fetchall()

        return all_data
    
    def filtered_item_data(self, text):
        self.cursor.execute('''
        SELECT DISTINCT
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
            LEFT JOIN Item ON ItemPrice.ItemId = Item.ItemId
            LEFT JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
            LEFT JOIN Brand ON Item.BrandId = Brand.BrandId
            LEFT JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
            LEFT JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
        WHERE
            Item.ItemName LIKE ? OR
            Item.Barcode LIKE ? OR
            ItemType.Name LIKE ? OR
            Brand.Name LIKE ? OR
            SalesGroup.Name LIKE ? OR
            Supplier.Name LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        item = self.cursor.fetchall()

        return item
    
# # for combo boxes in AddItemWindow
#     def filter_combobox_item_types(self, filter_text):
#         self.cursor.execute('''
#         SELECT DISTINCT Name FROM ItemType
#         WHERE Name LIKE ?
#         ORDER BY ItemTypeId DESC
#         ''', ('%' + filter_text + '%',))

#         item_types = [row[0] for row in self.cursor.fetchall()]
#         return item_types

#     def filter_combobox_brands(self, filter_text):
#         self.cursor.execute('''
#         SELECT DISTINCT Name FROM Brand
#         WHERE Name LIKE ?
#         ORDER BY BrandId DESC
#         ''', ('%' + filter_text + '%',))
        
#         brands = [row[0] for row in self.cursor.fetchall()]
#         return brands

#     def filter_combobox_sales_groups(self, filter_text):
#         self.cursor.execute('''
#         SELECT DISTINCT Name FROM SalesGroup
#         WHERE Name LIKE ?
#         ORDER BY SalesGroupId DESC
#         ''', ('%' + filter_text + '%',))
        
#         sales_groups = [row[0] for row in self.cursor.fetchall()]
#         return sales_groups

#     def filter_combobox_suppliers(self, filter_text):
#         self.cursor.execute('''
#         SELECT DISTINCT Name FROM Supplier
#         WHERE Name LIKE ?
#         ORDER BY SupplierId DESC
#         ''', ('%' + filter_text + '%',))
        
#         suppliers = [row[0] for row in self.cursor.fetchall()]
#         return suppliers
        
#     def filter_combobox_items(self, filter_text):
#         self.cursor.execute('''
#         SELECT DISTINCT ItemName FROM Item
#         WHERE ItemName LIKE ?
#         ORDER BY ItemId DESC
#         ''', ('%' + filter_text + '%',))
        
#         items = [row[0] for row in self.cursor.fetchall()]
        
#         return items


# for combo boxes in AddItemWindow
    def combobox_item_types(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM ItemType
        ORDER BY ItemTypeId DESC
        ''')

        item_types = [row[0] for row in self.cursor.fetchall()]
        return item_types

    def combobox_brands(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Brand
        ORDER BY BrandId DESC
        ''')
        
        brands = [row[0] for row in self.cursor.fetchall()]
        return brands

    def combobox_sales_groups(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM SalesGroup
        ORDER BY SalesGroupId DESC
        ''')
        
        sales_groups = [row[0] for row in self.cursor.fetchall()]
        return sales_groups

    def combobox_suppliers(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Supplier
        ORDER BY SupplierId DESC
        ''')
        
        suppliers = [row[0] for row in self.cursor.fetchall()]
        return suppliers
        
    def combobox_items(self):
        self.cursor.execute('''
        SELECT DISTINCT ItemName FROM Item
        ORDER BY ItemId DESC
        ''')
        
        items = [row[0] for row in self.cursor.fetchall()]
        
        return items
