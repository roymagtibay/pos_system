import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

# for storing item data


class InsertPromoData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/experimental_v6/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def InsertPromo(self, Name, Description, PromoType, PromoTypeValue):
        self.cursor.execute('''
        INSERT INTO Promo (Name, Description, PromoType, PromoTypeValue)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Promo
        WHERE
            Name = ? AND
            Description = ? AND
            PromoType = ? AND
            PromoTypeValue = ?
        )''', (Name, Description, PromoType, PromoTypeValue,
              Name, Description, PromoType, PromoTypeValue))
        self.conn.commit()

# for retrieving ids
#class SelectPromoId():
#    def __init__(self, db_file='SALES.db'):
#        super().__init__()
#        # Creates folder for the db file
#        self.db_folder_path = 'database/sales/'  # Adjust the path
#        self.db_file_path = os.path.join(self.db_folder_path, db_file)
#        os.makedirs(self.db_folder_path, exist_ok=True)
#
#        # Connects to SQL database named 'SALES.db'
#        self.conn = sqlite3.connect(database=self.db_file_path)
#        self.cursor = self.conn.cursor()
#
#    def item_type_id(self, item_type):
#        self.cursor.execute('''
#        SELECT PromoId FROM Promo
#        WHERE Name = ?
#        ''', (item_type,))
#
#        item_type_id = self.cursor.fetchone()
#
#        return item_type_id[0]
#
#    def brand_id(self, brand):
#        self.cursor.execute('''
#        SELECT BrandId FROM Brand
#        WHERE Name = ?
#        ''', (brand,))
#
#        brand_id = self.cursor.fetchone()
#
#        return brand_id[0]
#
#    def sales_group_id(self, sales_group):
#        self.cursor.execute('''
#        SELECT SalesGroupId FROM SalesGroup
#        WHERE Name = ?
#        ''', (sales_group,))
#
#        sales_group_id = self.cursor.fetchone()
#
#        return sales_group_id[0]
#
#    def supplier_id(self, supplier):
#        self.cursor.execute('''
#        SELECT SupplierId FROM Supplier
#        WHERE Name = ?
#        ''', (supplier,))
#
#        supplier_id = self.cursor.fetchone()
#
#        return supplier_id[0]
#
#    def item_id(self, item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id):
#        self.cursor.execute('''
#        SELECT ItemId FROM Item
#        WHERE ItemName = ? AND Barcode = ? AND ExpireDt = ? AND ItemTypeId = ? AND BrandId = ? AND SalesGroupId = ? AND SupplierId = ?
#        ''', (item_name, barcode, expire_dt, item_type_id, brand_id, sales_group_id, supplier_id))
#
#        item_id = self.cursor.fetchone()
#
#        return item_id[0]
#
#    def item_price_id(self, item_id, cost, discount, sell_price, effective_dt):
#        self.cursor.execute('''
#        SELECT ItemPriceId FROM ItemPrice
#        WHERE ItemId = ? AND Cost = ? AND Discount = ? AND SellPrice = ? AND EffectiveDt = ?
#        ''', (item_id, cost, discount, sell_price, effective_dt))
#
#        item_price_id = self.cursor.fetchone()
#
#        return item_price_id[0]

# for editing items
class UpdatePromoData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/experimental_v6/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def promo_data(self, Name, Description, PromoType, PromoTypeValue, oldname):
        self.cursor.execute('''
        UPDATE Promo
        SET Name = ?, Description = ?, PromoType = ?, PromoTypeValue = ?
        WHERE Name = ? 
        ''', (Name, Description, PromoType, PromoTypeValue, oldname))
        self.conn.commit()

# for listing data
class SelectPromoData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/experimental_v6/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def all_Promo_data(self):
        self.cursor.execute('''
        SELECT
            Name,
            Description, 
            PromoType,
            PromoTypeValue 
        FROM Promo
        ''')
        all_data = self.cursor.fetchall()
        return all_data
    
    def filtered_Promo_data(self, text):
        self.cursor.execute('''
        SELECT
            Name,
            Description, 
            PromoType,
            PromoTypeValue  
        FROM Promo
        WHERE
            Name LIKE ? OR Description LIKE ? OR PromoType LIKE ? OR PromoTypeValue LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        stock = self.cursor.fetchall()

        return stock
