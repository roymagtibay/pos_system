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

	def select_data(self):
		self.cursor.execute('''
		SELECT s.ItemPriceId, s.CustomerId, s.StockId, s.UserId, s.Quantity, s.TotalAmount, s.Void, s.ReferenceId, r.Reason
		FROM ItemSold s
		LEFT JOIN Reason r
		ON s.ReasonId = r.ReasonId            
		''')	
		data = self.cursor.fetchall()
		return data

	def insert_data(self, ItemPriceId, CustomerId, StockId, UserId, Quantity, TotalAmount, ReferenceId):
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

	def void_data(self, ItemPriceId, ReasonId, ReferenceId):
		self.cursor.execute('''
		UPDATE ItemSold
		SET Void = 1,
		    ResonId = ? 
		WHERE   ItemPriceId = ?   AND  ReferenceId = ?         
		''', (ReasonId, ItemPriceId, ReferenceId))	
		
		self.conn.commit()

class ReasonData():
	def __init__(self, db_file='SALES.db'):
		super().__init__()
		# creates folder for the db file
		self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/database/sales'
		self.db_file_path = os.path.join(self.db_folder_path, db_file)
		os.makedirs(self.db_folder_path, exist_ok=True)		
		# connects to SQL database named 'SALES.db'
		self.conn = sqlite3.connect(database=self.db_file_path)
		self.cursor = self.conn.cursor()

	def insert_data(self, Reason):
		self.cursor.execute('''
		INSERT INTO Reason (Reason)
		SELECT ?
		WHERE NOT EXISTS (SELECT 1 FROM Reason WHERE Reason = ?)      
		''', (Reason, Reason))	
		
		self.conn.commit()

	def select_data(self, Reason):
		self.cursor.execute('''
		SELECT ReasonId
		FROM Reason 
		WHERE Reason = ?      
		''', (Reason))
		data = self.cursor.fetchone()
		return data

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

	def update_points(self, ReferenceId, CustomerId, TotalAmount)
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