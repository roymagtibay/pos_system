import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

# for storing item data
class CustomerData():
    def __init__(self, db_file='sales.db'):
        super().__init__()
        # creates folder for the db file
        self.db_folder_path = 'C:/Users/User/Documents/GitHub/pos_system/customer/sales'
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def FetchDataByName(self, name):
        self.cursor.execute('''
        SELECT Address, Barrio, Town, Phone, Age, Gender, Marital_Status FROM Customer
        WHERE Fullname = ?
        ''', (name, ))
        data = self.cursor.fetchone()
        return data

    def SelectLikeNames(self, name):
        self.cursor.execute('''
        SELECT Fullname FROM Customer WHERE Fullname LIKE ?''', ('%' + name + '%',)
        )
        data = self.cursor.fetchall()
        return data

    def Insertdata(self, name, address, barrio, town, phone, age, gender, marital):
        self.cursor.execute('''
        INSERT INTO Customer (Fullname, Address, Barrio, Town, Phone, Age, Gender, Marital_Status)
        SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM Customer WHERE Fullname = ?)
        ''', (name, address, barrio, town, phone, age, gender, marital, name))
        self.conn.commit()

    def Updatedata(self, name, address, barrio, town, phone, age, gender, marital):
        self.cursor.execute('''
        UPDATE Customer 
        SET Address = ?,
            Barrio = ?,
            Town = ?,
            Phone = ?,
            Age = ?,
            Gender = ?,
            Marital_Status = ?,
            UpdateTs =  CURRENT_TIMESTAMP                
        WHERE Fullname = ?                                                                                                                   
        ''', (address, barrio, town, phone, age, gender, marital, name))
        self.conn.commit()