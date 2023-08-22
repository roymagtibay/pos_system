import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

# for storing item data
class UserDataCRUD():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/experimental_v6/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def select_user(self, level):
        self.cursor.execute('''
        SELECT Name , AccessLevel
        FROM User
        WHERE AccessLevel = ?
        ''', (level))
        all_data = self.cursor.fetchall()        
        return all_data
        
    
    def select_alluser(self):
        self.cursor.execute('''
        SELECT Name, AccessLevel
        FROM User
        ''')
        all_data = self.cursor.fetchall()
        return all_data

    def create_user(self, Name, Pwd, AccessLevel):
        self.cursor.execute('''
        INSERT INTO User (Name, Password, AccessLevel)
        SELECT ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM User
        WHERE
            Name = ?
        )''', (Name, Pwd, AccessLevel, Name))
        self.conn.commit()

    def update_user(self, Name, Password, AccessLevel):
        self.cursor.execute('''
        UPDATE User
        SET  AccessLevel = ?,
             Password = ?,
             UpdateTs = CURRENT_TIMESTAMP
        WHERE   Name = ?                                                        
        ''', (AccessLevel, Password, Name))
        self.conn.commit()

    def delete_user(self, Name):
        self.cursor.execute('''
        DELETE User
        WHERE   Name = ?                                                        
        )''', (Name))
        self.conn.commit()    
