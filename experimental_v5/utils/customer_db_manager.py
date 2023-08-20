import os
import sqlite3 # pre-installed in python (if not, install it using 'pip install pysqlite')
import os 

class ManageCustomerData():
    def __init__(self, db_file='SALES.db'):
        super().__init__()
        # Creates folder for the db file
        self.db_folder_path = 'database/sales/'  # Adjust the path
        self.db_file_path = os.path.join(self.db_folder_path, db_file)
        os.makedirs(self.db_folder_path, exist_ok=True)

        # Connects to SQL database named 'SALES.db'
        self.conn = sqlite3.connect(database=self.db_file_path)
        self.cursor = self.conn.cursor()

    def retreive_all_data(self, name):
        self.cursor.execute('''
        SELECT CustomerId, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus FROM Customer
        WHERE CustomerName = ?
        ''', (name,))
        all_customer_data = self.cursor.fetchall()
        return all_customer_data

    def retrieve_customer_name(self, customer_id):
        self.cursor.execute('''
        SELECT CustomerName FROM Customer
        WHERE CustomerId = ?
        ''', (customer_id,))

    def store_all_data(self, name, address, barrio, town, phone, age, gender, marital_status):
        self.cursor.execute('''
        INSERT INTO Customer (CustomerName, Address, Barrio, Town, Phone, Age, Gender, MaritalStatus)
        SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT 1 FROM Customer WHERE CustomerName = ?)
        ''', (name, address, barrio, town, phone, age, gender, marital_status, name))
        self.conn.commit()

    def change_all_data(self, name, address, barrio, town, phone, age, gender, marital_status):
        self.cursor.execute('''
        UPDATE Customer 
        SET Address = ?,
            Barrio = ?,
            Town = ?,
            Phone = ?,
            Age = ?,
            Gender = ?,
            MaritalStatus = ?,
            UpdateTs =  CURRENT_TIMESTAMP                
        WHERE CustomerName = ?                                                                                                                   
        ''', (address, barrio, town, phone, age, gender, marital_status, name))
        self.conn.commit()