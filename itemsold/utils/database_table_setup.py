import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

class CreateDatabaseTable():
    def __init__(self, db_file='TXN.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/txn/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'TXN.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def database_table(self):
        
        self.cursor.execute('''
		CREATE TABLE IF NOT EXISTS ItemSold (
			ItemSoldId INTEGER PRIMARY KEY AUTOINCREMENT,
			ItemPriceId INTEGER DEFAULT 0,
			CustomerId INTEGER DEFAULT 0,
			StockId INTEGER DEFAULT 0,
			UserId INTEGER DEFAULT 0,
			Quantity INTEGER,
			TotalAmount DECIMAL(15, 2),
			Void BIT DEFAULT 0,
			ReferenceId TEXT,
			UpdateTs DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (ItemPriceId) REFERENCES ItemPrice(ItemPriceId),
			FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId),
			FOREIGN KEY (StockId) REFERENCES Stocks(StockId)
		);
        ''')
        self.conn.commit()
