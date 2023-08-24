import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

class ItemSoldData():
	def __init__(self, db_file='TXN.db'):
		super().__init__()
		# creates folder for the db file
		self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/database/txn'
		self.db_file_path = os.path.join(self.db_folder_path, db_file)
		os.makedirs(self.db_folder_path, exist_ok=True)		
		# connects to SQL database named 'TXN.db'
		self.conn = sqlite3.connect(database=self.db_file_path)
		self.cursor = self.conn.cursor()
		
	def InsertItemSold(self, ItemPriceId, CustomerId, StockId, UserId, Quantity, TotalAmount, ReferenceId):
		self.cursor.execute('''
		INSERT INTO ItemSold (ItemPriceId, CustomerId, StockId, UserId, Quantity, TotalAmount, ReferenceId)
		SELECT 
			p.ItemPriceId?,
			c.CustomerId?,
			s.StockId?,
			u.UserId?,
			Quantity?,
			TotalAmount?,
			ReferenceId?
		''', (ItemPriceId, CustomerId, StockId, UserId, Quantity, TotalAmount, ReferenceId))	
		
		self.conn.commit()

class CustomerData():
	def __init__(self, db_file='SALES.db'):
		super().__init__()
		# creates folder for the db file
		self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/database/sales'
		self.db_file_path = os.path.join(self.db_folder_path, db_file)
		os.makedirs(self.db_folder_path, exist_ok=True)		
		# connects to SQL database named 'SALES.db'
		self.conn = sqlite3.connect(database=self.db_file_path)
		self.cursor = self.conn.cursor()

	def UpdateCustomer(self, ReferenceId, CustomerId, TotalAmount)
		self.cursor.execute('''
		UPDATE Customer
		SET Points = Points + (
						SELECT 
							r.Point + ((TotalAmount? - r.Unit) * (SELECT COALESCE(r.Point,0) FROM Reward r WHERE r.Unit = 1) as totalPoints
							
						FROM ItemSold s
						
						CROSS JOIN Reward r  
						INNER JOIN Customer c  ON s.CustomerId = c.CustomerId
						
						WHERE s.ReferenceId = ReferenceId?
						AND s.CustomerId = CustomerId?
						AND s.TotalAmount? >= r.Unit 
						
						ORDER BY r.Unit DESC
						LIMIT 1
					),
		UpdateTs = CURRENT_TIMESTAMP			
		WHERE CustomerId = CustomerId?
		''', (ReferenceId, CustomerId, TotalAmount))

		self.conn.commit()