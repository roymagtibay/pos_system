import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

# for storing item data


class InsertRewardData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def InsertReward(self, Name, Description, Unit, Point):
        self.cursor.execute('''
        INSERT INTO Reward (Name, Description, Unit, Point)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS(
        SELECT 1 FROM Reward
        WHERE
            Name = ? AND
            Description = ? AND
            Unit = ? AND
            Point = ?
        )''', (Name, Description, Unit, Point,
              Name, Description, Unit, Point))
        self.conn.commit()


# for editing items
class UpdateRewardData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def Reward_data(self, Name, Description, Unit, Point, oldname):
        self.cursor.execute('''
        UPDATE Reward
        SET Name = ?, Description = ?, Unit = ?, Point = ?
        WHERE Name = ? 
        ''', (Name, Description, Unit, Point, oldname))
        self.conn.commit()

# for listing data
class SelectRewardData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/database/sales'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def all_Reward_data(self):
        self.cursor.execute('''
        SELECT
            Name,
            Description, 
            Unit,
            Point 
        FROM Reward
        ''')
        all_data = self.cursor.fetchall()
        return all_data
    
    def filtered_Reward_data(self, text):
        self.cursor.execute('''
        SELECT
            Name,
            Description, 
            Unit,
            Point  
        FROM Reward
        WHERE
            Name LIKE ? OR Description LIKE ? OR Unit LIKE ? OR Point LIKE ?
        ''', ('%' + text + '%', '%' + text + '%', '%' + text + '%', '%' + text + '%'))

        stock = self.cursor.fetchall()

        return stock
