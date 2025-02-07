import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')

class ItemManagementSQL():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

# for storing item data
    def insertItemTypeData(self, item_type):
        self.cursor.execute('''
        INSERT INTO ItemType (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM ItemType WHERE Name = ?)
        ''', (item_type, item_type))
        self.conn.commit()

    def insertBrandData(self, brand):
        self.cursor.execute('''
        INSERT INTO Brand (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Brand WHERE Name = ?)
        ''', (brand, brand))
        self.conn.commit()
    
    def insertSalesGroupData(self, sales_group):
        self.cursor.execute('''
        INSERT INTO SalesGroup (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM SalesGroup WHERE Name = ?)
        ''', (sales_group, sales_group))
        self.conn.commit()

    def insertSupplierData(self, supplier):
        self.cursor.execute('''
        INSERT INTO Supplier (Name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM Supplier WHERE Name = ?)
        ''', (supplier, supplier))
        self.conn.commit()

    def insertItemData(self, barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        INSERT INTO Item (Barcode, ItemName, ExpireDt, ItemTypeId, BrandId, SalesGroupId, SupplierId)
        SELECT ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Item
            INNER JOIN ItemType ON Item.ItemTypeId = ItemType.ItemTypeId
            INNER JOIN Brand ON Item.BrandId = Brand.BrandId
            INNER JOIN SalesGroup ON Item.SalesGroupId = SalesGroup.SalesGroupId
            INNER JOIN Supplier ON Item.SupplierId = Supplier.SupplierId
        WHERE
            Item.Barcode = ? AND
            Item.ItemName = ? AND
            Item.ExpireDt = ? AND
            Item.ItemTypeId = ? AND
            Item.BrandId = ? AND
            Item.SupplierId = ? AND
            Item.SalesGroupId = ?
        )''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id,
              barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
        self.conn.commit()

    def insertItemPriceData(self, item_id, cost, discount, sell_price, effective_dt):
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
    def selectItemTypeId(self, item_type):
        self.cursor.execute('''
        SELECT ItemTypeId FROM ItemType
        WHERE Name = ?
        ''', (item_type,))

        item_type_id = self.cursor.fetchone()

        return item_type_id[0]

    def selectBrandId(self, brand):
        self.cursor.execute('''
        SELECT BrandId FROM Brand
        WHERE Name = ?
        ''', (brand,))

        brand_id = self.cursor.fetchone()

        return brand_id[0]

    def selectSalesGroupId(self, sales_group):
        self.cursor.execute('''
        SELECT SalesGroupId FROM SalesGroup
        WHERE Name = ?
        ''', (sales_group,))

        sales_group_id = self.cursor.fetchone()

        return sales_group_id[0]

    def selectSupplierId(self, supplier):
        self.cursor.execute('''
        SELECT SupplierId FROM Supplier
        WHERE Name = ?
        ''', (supplier,))

        supplier_id = self.cursor.fetchone()

        return supplier_id[0]

    def selectItemId(self, barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        SELECT ItemId FROM Item
        WHERE Barcode = ? AND ItemName = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
        ''', (barcode, item_name, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))

        item_id = self.cursor.fetchone()

        return item_id[0]

    def selectItemPriceId(self, item_id, cost, discount, sell_price, effective_dt):
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
    def updateItemData(self, barcode, item_name, expire_dt, item_id, item_type_id, brand_id, sales_group_id, supplier_id):
        self.cursor.execute('''
        UPDATE Item
        SET Barcode = ?,
            ItemName = ?,
            ExpireDt = ?
        WHERE ItemId = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?;
        ''', (barcode, item_name, expire_dt, item_id, item_type_id, brand_id, sales_group_id, supplier_id))

        self.conn.commit()

# for listing data
    def selectAllItemData(self, text):
        self.cursor.execute('''
        SELECT
            COALESCE(Item.Barcode, 'unk'),
            COALESCE(Item.ItemName, 'unk'),
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
            Item.Barcode LIKE ? OR
            Item.ItemName LIKE ? OR
            ItemType.Name LIKE ? OR
            Brand.Name LIKE ? OR
            SalesGroup.Name LIKE ? OR
            Supplier.Name LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))
        
        all_data = self.cursor.fetchall()

        return all_data
    
    def selectAllFilteredItemData(self, text):
        self.cursor.execute('''
        SELECT DISTINCT
            COALESCE(Item.Barcode, 'unk'),
            COALESCE(Item.ItemName, 'unk'),
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
            Item.Barcode LIKE ? OR
            Item.ItemName LIKE ? OR
            ItemType.Name LIKE ? OR
            Brand.Name LIKE ? OR
            SalesGroup.Name LIKE ? OR
            Supplier.Name LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        item = self.cursor.fetchall()

        return item
    
# for combo boxes in AddItemWindow
    def selectItemTypeData(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM ItemType
        ORDER BY ItemTypeId DESC
        ''')

        item_types = [row[0] for row in self.cursor.fetchall()]
        return item_types

    def selectBrandData(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Brand
        ORDER BY BrandId DESC
        ''')
        
        brands = [row[0] for row in self.cursor.fetchall()]
        return brands

    def selectSalesGroupData(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM SalesGroup
        ORDER BY SalesGroupId DESC
        ''')
        
        sales_groups = [row[0] for row in self.cursor.fetchall()]
        return sales_groups

    def selectSupplierData(self):
        self.cursor.execute('''
        SELECT DISTINCT Name FROM Supplier
        ORDER BY SupplierId DESC
        ''')
        
        suppliers = [row[0] for row in self.cursor.fetchall()]
        return suppliers
        
    def selectItemData(self):
        self.cursor.execute('''
        SELECT DISTINCT ItemName FROM Item
        ORDER BY ItemId DESC
        ''')
        
        items = [row[0] for row in self.cursor.fetchall()]
        
        return items
