# import mysql.connector
# from mysql.connector import errorcode
# import pandas as pd
# import os
# from decimal import Decimal
# from datetime import datetime

# # -------------------- Configuration --------------------

# # MySQL server connection details
# MYSQL_CONFIG = {
#     'user': 'root',
#     'password': '123456789',
#     'host': 'localhost',  # e.g., 'localhost' or '127.0.0.1'
#     'port': 3306,         # Default MySQL port is 3306
# }

# # Directory where CSV files are stored
# CSV_DIRECTORY = r'D:\IIA_Project'  # Use raw string or escape backslashes

# # -------------------- Database and Table Definitions --------------------

# DATABASES = {
#     'MutualFundsDB': {
#         'tables': {
#             'MutualFunds': {
#                 'csv_file': 'MutualFunds.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS MutualFunds (
#                         MutualFundID INT PRIMARY KEY,
#                         FundName VARCHAR(255) UNIQUE,
#                         Category VARCHAR(100),
#                         RiskProfile VARCHAR(50),
#                         ManagerName VARCHAR(255)
#                     );
#                 """
#             },
#             'MutualFundRates': {
#                 'csv_file': 'MutualFundRates.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS MutualFundRates (
#                         RateID INT AUTO_INCREMENT PRIMARY KEY,
#                         MutualFundID INT,
#                         RateDate DATE,
#                         RatePerQuantity DECIMAL(10,4),
#                         FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'SBI_MF_Clients': {
#                 'csv_file': 'SBI_MF_Clients.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_MF_Clients (
#                         SBI_ClientID INT PRIMARY KEY,
#                         FullName VARCHAR(255),
#                         ClientEmail VARCHAR(255) UNIQUE,
#                         ContactNumber VARCHAR(50),
#                         PAN_Number VARCHAR(20) UNIQUE,
#                         Address VARCHAR(500),
#                         DateOfBirth DATE,
#                         RegistrationDate DATE
#                     );
#                 """
#             },
#             'TataMF_Investors': {
#                 'csv_file': 'TataMF_Investors.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS TataMF_Investors (
#                         Tata_ClientID INT PRIMARY KEY,
#                         InvestorName VARCHAR(255),
#                         EmailAddress VARCHAR(255) UNIQUE,
#                         PhoneNumber VARCHAR(50),
#                         PAN VARCHAR(20) UNIQUE,
#                         ResidentialAddress VARCHAR(500),
#                         DOB DATE,
#                         JoinDate DATE
#                     );
#                 """
#             },
#             'BajajMF_Customers': {
#                 'csv_file': 'BajajMF_Customers.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS BajajMF_Customers (
#                         Bajaj_CustomerID INT PRIMARY KEY,
#                         Name VARCHAR(255),
#                         Email VARCHAR(255) UNIQUE,
#                         Mobile VARCHAR(50),
#                         PAN_Num VARCHAR(20) UNIQUE,
#                         Addr VARCHAR(500),
#                         DOB DATE,
#                         DateJoined DATE
#                     );
#                 """
#             },
#             'SBI_MF_Returns': {
#                 'csv_file': 'SBI_MF_Returns.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_MF_Returns (
#                         ReturnID INT PRIMARY KEY,
#                         MutualFundID INT,
#                         SBI_ClientID INT,
#                         InvestmentDate DATE,
#                         UnitsPurchased DECIMAL(10,4),
#                         InvestmentAmount DECIMAL(15,2),
#                         PurchaseRate DECIMAL(10,4),
#                         CurrentNAV DECIMAL(10,4),
#                         CurrentValue DECIMAL(15,2),
#                         ReturnPercentage DECIMAL(5,2),
#                         LastUpdated DATE,
#                         FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID)
#                             ON DELETE CASCADE ON UPDATE CASCADE,
#                         FOREIGN KEY (SBI_ClientID) REFERENCES SBI_MF_Clients(SBI_ClientID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'TataMF_InvestmentReturns': {
#                 'csv_file': 'TataMF_InvestmentReturns.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS TataMF_InvestmentReturns (
#                         InvestmentReturnID INT PRIMARY KEY,
#                         MutualFundID INT,
#                         Tata_ClientID INT,
#                         DateOfInvestment DATE,
#                         UnitsBought DECIMAL(10,4),
#                         InvestmentINR DECIMAL(15,2),
#                         PurchaseRate DECIMAL(10,4),
#                         CurrentNAVValue DECIMAL(10,4),
#                         InvestmentValue DECIMAL(15,2),
#                         GainLossPercentage DECIMAL(5,2),
#                         LastUpdated DATE,
#                         FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID)
#                             ON DELETE CASCADE ON UPDATE CASCADE,
#                         FOREIGN KEY (Tata_ClientID) REFERENCES TataMF_Investors(Tata_ClientID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'BajajMF_ClientReturns': {
#                 'csv_file': 'BajajMF_ClientReturns.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS BajajMF_ClientReturns (
#                         ClientReturnID INT PRIMARY KEY,
#                         MutualFundID INT,
#                         Bajaj_CustomerID INT,
#                         InvestmentDate DATE,
#                         UnitsPurchased DECIMAL(10,4),
#                         AmountInvested DECIMAL(15,2),
#                         PurchaseRate DECIMAL(10,4),
#                         CurrentNAV DECIMAL(10,4),
#                         CurrentValue DECIMAL(15,2),
#                         ProfitLossPerc DECIMAL(5,2),
#                         UpdateDate DATE,
#                         FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID)
#                             ON DELETE CASCADE ON UPDATE CASCADE,
#                         FOREIGN KEY (Bajaj_CustomerID) REFERENCES BajajMF_Customers(Bajaj_CustomerID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#         }
#     },
#     'StockPlatformsDB': {
#         'tables': {
#             'Zerodha_Clients': {
#                 'csv_file': 'Zerodha_Clients.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Zerodha_Clients (
#                         Zerodha_ClientID INT PRIMARY KEY,
#                         ClientName VARCHAR(255),
#                         Email VARCHAR(255) UNIQUE,
#                         PhoneNumber VARCHAR(50),
#                         PAN VARCHAR(20) UNIQUE,
#                         Address VARCHAR(500),
#                         DateOfBirth DATE,
#                         AccountCreationDate DATE
#                     );
#                 """
#             },
#             'Zerodha_Stocks': {
#                 'csv_file': 'Zerodha_Stocks.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Zerodha_Stocks (
#                         Zerodha_StockID INT PRIMARY KEY,
#                         StockSymbol VARCHAR(20) UNIQUE,
#                         StockName VARCHAR(255),
#                         Sector VARCHAR(100),
#                         Exchange VARCHAR(50)
#                     );
#                 """
#             },
#             'Zerodha_Orders': {
#                 'csv_file': 'Zerodha_Orders.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Zerodha_Orders (
#                         OrderID INT PRIMARY KEY,
#                         ClientID INT,
#                         StockID INT,
#                         OrderType VARCHAR(10),
#                         Quantity INT,
#                         PricePerShare DECIMAL(15,2),
#                         TotalAmount DECIMAL(15,2),
#                         OrderDate DATETIME,
#                         OrderStatus VARCHAR(20),
#                         FOREIGN KEY (ClientID) REFERENCES Zerodha_Clients(Zerodha_ClientID)
#                             ON DELETE CASCADE ON UPDATE CASCADE,
#                         FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'Zerodha_Stock_Prices': {
#                 'csv_file': 'Zerodha_Stock_Prices.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Zerodha_Stock_Prices (
#                         PriceID INT AUTO_INCREMENT PRIMARY KEY,
#                         StockID INT,
#                         Date DATE,
#                         OpenPrice DECIMAL(15,2),
#                         ClosePrice DECIMAL(15,2),
#                         HighPrice DECIMAL(15,2),
#                         LowPrice DECIMAL(15,2),
#                         Volume BIGINT,
#                         LastUpdated DATETIME,
#                         FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'Groww_Clients': {
#                 'csv_file': 'Groww_Clients.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Groww_Clients (
#                         Groww_ClientID INT PRIMARY KEY,
#                         ClientName VARCHAR(255),
#                         Email VARCHAR(255) UNIQUE,
#                         PhoneNumber VARCHAR(50),
#                         PAN VARCHAR(20) UNIQUE,
#                         Address VARCHAR(500),
#                         DateOfBirth DATE,
#                         AccountCreationDate DATE
#                     );
#                 """
#             },
#             'Groww_Stocks': {
#                 'csv_file': 'Groww_Stocks.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Groww_Stocks (
#                         Groww_StockID INT PRIMARY KEY,
#                         Symbol VARCHAR(20) UNIQUE,
#                         Name VARCHAR(255),
#                         Sector VARCHAR(100),
#                         Exchange VARCHAR(50)
#                     );
#                 """
#             },
#             'Groww_Orders': {
#                 'csv_file': 'Groww_Orders.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Groww_Orders (
#                         OrderID INT PRIMARY KEY,
#                         ClientID INT,
#                         StockID INT,
#                         Type VARCHAR(10),
#                         Quantity INT,
#                         Price DECIMAL(15,2),
#                         TotalValue DECIMAL(15,2),
#                         Timestamp DATETIME,
#                         Status VARCHAR(20),
#                         FOREIGN KEY (ClientID) REFERENCES Groww_Clients(Groww_ClientID)
#                             ON DELETE CASCADE ON UPDATE CASCADE,
#                         FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'Groww_Stock_Prices': {
#                 'csv_file': 'Groww_Stock_Prices.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS Groww_Stock_Prices (
#                         PriceID INT AUTO_INCREMENT PRIMARY KEY,
#                         StockID INT,
#                         Date DATE,
#                         Open DECIMAL(15,2),
#                         Close DECIMAL(15,2),
#                         High DECIMAL(15,2),
#                         Low DECIMAL(15,2),
#                         Volume BIGINT,
#                         LastUpdated DATETIME,
#                         FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'SBI_Stocks_Clients': {
#                 'csv_file': 'SBI_Stocks_Clients.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_Stocks_Clients (
#                         SBI_ClientID INT PRIMARY KEY,
#                         ClientName VARCHAR(255),
#                         Email VARCHAR(255) UNIQUE,
#                         PhoneNumber VARCHAR(50),
#                         PAN VARCHAR(20) UNIQUE,
#                         Address VARCHAR(500),
#                         DateOfBirth DATE,
#                         AccountStartDate DATE
#                     );
#                 """
#             },
#             'SBI_Stocks_List': {
#                 'csv_file': 'SBI_Stocks_List.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_Stocks_List (
#                         SBI_StockID INT PRIMARY KEY,
#                         StockCode VARCHAR(20) UNIQUE,
#                         StockName VARCHAR(255),
#                         Sector VARCHAR(100),
#                         Exchange VARCHAR(50)
#                     );
#                 """
#             },
#             'SBI_Stocks_Orders': {
#                 'csv_file': 'SBI_Stocks_Orders.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_Stocks_Orders (
#                         OrderID INT PRIMARY KEY,
#                         ClientID INT,
#                         StockID INT,
#                         TradeType VARCHAR(10),
#                         Quantity INT,
#                         PricePerShare DECIMAL(15,2),
#                         TotalValue DECIMAL(15,2),
#                         TradeTimestamp DATETIME,
#                         TradeStatus VARCHAR(20),
#                         FOREIGN KEY (ClientID) REFERENCES SBI_Stocks_Clients(SBI_ClientID)
#                             ON DELETE CASCADE ON UPDATE CASCADE,
#                         FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'SBI_Stocks_Prices': {
#                 'csv_file': 'SBI_Stocks_Prices.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_Stocks_Prices (
#                         PriceID INT AUTO_INCREMENT PRIMARY KEY,
#                         StockID INT,
#                         Date DATE,
#                         Open_Price DECIMAL(15,2),
#                         Close_Price DECIMAL(15,2),
#                         High_Price DECIMAL(15,2),
#                         Low_Price DECIMAL(15,2),
#                         Trade_Volume BIGINT,
#                         LastUpdated DATETIME,
#                         FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#         }
#     },
#     'BanksDB': {
#         'tables': {
#             'ICICI_Accounts': {
#                 'csv_file': 'ICICI_Accounts.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS ICICI_Accounts (
#                         ICICI_AccountID INT PRIMARY KEY,
#                         CustomerName VARCHAR(255),
#                         AccountNumber VARCHAR(50) UNIQUE,
#                         ServiceType VARCHAR(50),
#                         NationalID VARCHAR(20) UNIQUE,
#                         Balance DECIMAL(15,2),
#                         InterestRate DECIMAL(5,2),
#                         LastUpdated DATE
#                     );
#                 """
#             },
#             'HDFC_Accounts': {
#                 'csv_file': 'HDFC_Accounts.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS HDFC_Accounts (
#                         HDFC_AccountID INT PRIMARY KEY,
#                         ClientName VARCHAR(255),
#                         AccNo VARCHAR(50) UNIQUE,
#                         AccountType VARCHAR(50),
#                         GovtID VARCHAR(20) UNIQUE,
#                         CurrentBalance DECIMAL(15,2),
#                         MonthlyInterest DECIMAL(5,2),
#                         LastUpdate DATE
#                     );
#                 """
#             },
#             'SBI_Accounts': {
#                 'csv_file': 'SBI_Accounts.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_Accounts (
#                         SBI_AccountID INT PRIMARY KEY,
#                         AccountHolder VARCHAR(255),
#                         Acc_Number VARCHAR(50) UNIQUE,
#                         Service_Type VARCHAR(50),
#                         National_ID VARCHAR(20) UNIQUE,
#                         AmountStored DECIMAL(15,2),
#                         Interest_Rate DECIMAL(5,2),
#                         Last_Updated DATE
#                     );
#                 """
#             },
#             'ICICI_Transactions': {
#                 'csv_file': 'ICICI_Transactions.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS ICICI_Transactions (
#                         TransactionID INT PRIMARY KEY,
#                         ICICI_AccountID INT,
#                         TransactionDate DATE,
#                         TransactionType VARCHAR(20),
#                         Amount DECIMAL(15,2),
#                         Description VARCHAR(500),
#                         FOREIGN KEY (ICICI_AccountID) REFERENCES ICICI_Accounts(ICICI_AccountID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'HDFC_Transactions': {
#                 'csv_file': 'HDFC_Transactions.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS HDFC_Transactions (
#                         TransactionID INT PRIMARY KEY,
#                         HDFC_AccountID INT,
#                         TransDate DATE,
#                         Type VARCHAR(20),
#                         TransAmount DECIMAL(15,2),
#                         Notes VARCHAR(500),
#                         FOREIGN KEY (HDFC_AccountID) REFERENCES HDFC_Accounts(HDFC_AccountID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#             'SBI_Transactions': {
#                 'csv_file': 'SBI_Transactions.csv',
#                 'create_table_sql': """
#                     CREATE TABLE IF NOT EXISTS SBI_Transactions (
#                         TransactionID INT PRIMARY KEY,
#                         SBI_AccountID INT,
#                         Date DATE,
#                         Type_of_Transaction VARCHAR(20),
#                         Amount DECIMAL(15,2),
#                         Details VARCHAR(500),
#                         FOREIGN KEY (SBI_AccountID) REFERENCES SBI_Accounts(SBI_AccountID)
#                             ON DELETE CASCADE ON UPDATE CASCADE
#                     );
#                 """
#             },
#         }
#     }
# }

# # -------------------- Utility Functions --------------------

# def connect_to_mysql(config):
#     """
#     Establish a connection to the MySQL server.
#     """
#     try:
#         cnx = mysql.connector.connect(**config)
#         print("Successfully connected to MySQL server.")
#         return cnx
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Access denied: Check your username or password.")
#         else:
#             print(f"Error: {err}")
#         exit(1)

# def create_database(cursor, db_name):
#     """
#     Create a new database if it does not exist.
#     """
#     try:
#         cursor.execute(
#             f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';"
#         )
#         print(f"Database `{db_name}` is ready.")
#     except mysql.connector.Error as err:
#         print(f"Failed creating database `{db_name}`: {err}")
#         exit(1)

# def create_table(cursor, create_table_sql, table_name):
#     """
#     Create a table using the provided SQL statement.
#     """
#     try:
#         cursor.execute(create_table_sql)
#         print(f"Table `{table_name}` created or already exists.")
#     except mysql.connector.Error as err:
#         print(f"Failed creating table `{table_name}`: {err}")
#         exit(1)

# def insert_data(cursor, table_name, df):
#     """
#     Insert data from a pandas DataFrame into a MySQL table.
#     """
#     # Generate the placeholder string
#     placeholders = ", ".join(["%s"] * len(df.columns))
#     columns = ", ".join([f"`{col}`" for col in df.columns])
#     insert_stmt = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

#     # Prepare the data as a list of tuples
#     data = []
#     for _, row in df.iterrows():
#         row_data = []
#         for col in df.columns:
#             value = row[col]
#             # Handle NaN values
#             if pd.isna(value):
#                 row_data.append(None)
#             elif isinstance(value, float):
#                 row_data.append(Decimal(str(value)))
#             elif isinstance(value, int):
#                 row_data.append(int(value))
#             elif isinstance(value, datetime):
#                 row_data.append(value)
#             else:
#                 row_data.append(str(value))
#         data.append(tuple(row_data))

#     try:
#         cursor.executemany(insert_stmt, data)
#         print(f"Inserted {cursor.rowcount} rows into `{table_name}`.")
#     except mysql.connector.Error as err:
#         print(f"Error inserting data into `{table_name}`: {err}")
#         raise

# # -------------------- Main Script --------------------

# def main():
#     # Connect to MySQL server
#     cnx = connect_to_mysql(MYSQL_CONFIG)
#     cursor = cnx.cursor()

#     # Iterate over each database
#     for db_name, db_info in DATABASES.items():
#         print(f"\n--- Processing Database: `{db_name}` ---")
#         # Create database
#         create_database(cursor, db_name)

#         # Use the created database
#         try:
#             cursor.execute(f"USE `{db_name}`;")
#             print(f"Switched to database `{db_name}`.")
#         except mysql.connector.Error as err:
#             print(f"Database `{db_name}` does not exist.")
#             exit(1)

#         # Determine table creation order based on dependencies
#         # Parent tables should be created before child tables
#         # For MutualFundsDB and StockPlatformsDB, MutualFunds and Stocks lists are parents
#         # Similarly for BanksDB, Accounts are parents to Transactions

#         # Create a list to define the order
#         if db_name == 'MutualFundsDB':
#             table_order = ['MutualFunds', 'MutualFundRates',
#                           'SBI_MF_Clients', 'TataMF_Investors', 'BajajMF_Customers',
#                           'SBI_MF_Returns', 'TataMF_InvestmentReturns', 'BajajMF_ClientReturns']
#         elif db_name == 'StockPlatformsDB':
#             table_order = ['Zerodha_Clients', 'Zerodha_Stocks', 'Zerodha_Orders', 'Zerodha_Stock_Prices',
#                           'Groww_Clients', 'Groww_Stocks', 'Groww_Orders', 'Groww_Stock_Prices',
#                           'SBI_Stocks_Clients', 'SBI_Stocks_List', 'SBI_Stocks_Orders', 'SBI_Stocks_Prices']
#         elif db_name == 'BanksDB':
#             table_order = ['ICICI_Accounts', 'HDFC_Accounts', 'SBI_Accounts',
#                           'ICICI_Transactions', 'HDFC_Transactions', 'SBI_Transactions']
#         else:
#             table_order = list(db_info['tables'].keys())

#         # Iterate over each table in the defined order
#         for table_name in table_order:
#             if table_name not in db_info['tables']:
#                 print(f"Table `{table_name}` not found in database `{db_name}` definitions.")
#                 continue

#             table_info = db_info['tables'][table_name]
#             csv_file = table_info['csv_file']
#             create_table_sql = table_info['create_table_sql']

#             print(f"\nCreating table `{table_name}`...")
#             # Create the table
#             try:
#                 create_table(cursor, create_table_sql, table_name)
#             except mysql.connector.Error as err:
#                 print(f"Failed creating table `{table_name}`: {err}")
#                 continue  # Skip to the next table

#             # Path to the CSV file
#             csv_path = os.path.join(CSV_DIRECTORY, csv_file)

#             # Check if the CSV file exists
#             if not os.path.exists(csv_path):
#                 print(f"CSV file `{csv_file}` not found in `{CSV_DIRECTORY}`. Skipping table `{table_name}`.")
#                 continue

#             # Read the CSV file into a pandas DataFrame
#             try:
#                 df = pd.read_csv(csv_path)
#                 print(f"Successfully read `{csv_file}` with {len(df)} records.")
#             except Exception as e:
#                 print(f"Error reading `{csv_file}`: {e}")
#                 continue

#             # Insert data into the table
#             try:
#                 insert_data(cursor, table_name, df)
#                 # Commit after each table insertion
#                 cnx.commit()
#             except Exception as e:
#                 print(f"Error inserting data into `{table_name}`: {e}")
#                 cnx.rollback()

#     # Close cursor and connection
#     cursor.close()
#     cnx.close()
#     print("\nData insertion completed successfully.")

# if __name__ == "__main__":
#     main()





import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# MySQL server connection configuration
config = {
    'user': 'root',
    'password': '123456789',  # Replace with your MySQL password
    'host': 'localhost',
    'raise_on_warnings': True
}

# List of databases to create
databases = ['Banks', 'MutualFunds', 'StockPlatforms']

# Dictionary to hold DataFrames for each database
dataframes = {}

# CSV files mapping for each database
csv_files = {
    'Banks': [
        'ICICI_Accounts.csv',
        'ICICI_Transactions.csv',
        'HDFC_Accounts.csv',
        'HDFC_Transactions.csv',
        'SBI_Accounts.csv',
        'SBI_Transactions.csv'
    ],
    'MutualFunds': [
        'MutualFunds.csv',
        'MutualFundRates.csv',
        'SBI_MF_Clients.csv',
        'SBI_MF_Returns.csv',
        'TataMF_Investors.csv',
        'TataMF_InvestmentReturns.csv',
        'BajajMF_Customers.csv',
        'BajajMF_ClientReturns.csv'
    ],
    'StockPlatforms': [
        'Zerodha_Clients.csv',
        'Zerodha_Stocks.csv',
        'Zerodha_Orders.csv',
        'Zerodha_Stock_Prices.csv',
        'Groww_Clients.csv',
        'Groww_Stocks.csv',
        'Groww_Orders.csv',
        'Groww_Stock_Prices.csv',
        'SBI_Stocks_Clients.csv',
        'SBI_Stocks_List.csv',
        'SBI_Stocks_Orders.csv',
        'SBI_Stocks_Prices.csv'
    ]
}

# Connect to MySQL server
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Connected to MySQL server.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Create databases
for db_name in databases:
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database '{db_name}': {err}")
        exit(1)

# Function to read CSV files into DataFrames
def read_csv_files(db_name):
    db_dataframes = {}
    for file_name in csv_files[db_name]:
        try:
            df = pd.read_csv(file_name)
            db_dataframes[file_name] = df
            print(f"Loaded '{file_name}' into DataFrame.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)
    return db_dataframes

# Function to create tables and insert data for a given database
def setup_database(db_name):
    cursor.execute(f"USE {db_name}")
    print(f"Using database '{db_name}'.")
    
    db_dataframes = read_csv_files(db_name)
    
    if db_name == 'Banks':
        setup_banks(db_dataframes)
    elif db_name == 'MutualFunds':
        setup_mutual_funds(db_dataframes)
    elif db_name == 'StockPlatforms':
        setup_stock_platforms(db_dataframes)
    else:
        print(f"No setup function for database '{db_name}'.")

# Function to setup Banks database
def setup_banks(db_dataframes):
    # Create ICICI tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ICICI_Accounts (
            ICICI_AccountID INT PRIMARY KEY,
            CustomerName VARCHAR(100),
            AccountNumber VARCHAR(50),
            ServiceType VARCHAR(50),
            NationalID VARCHAR(20),
            Balance FLOAT,
            InterestRate FLOAT,
            LastUpdated DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ICICI_Transactions (
            TransactionID INT PRIMARY KEY,
            ICICI_AccountID INT,
            TransactionDate DATE,
            TransactionType VARCHAR(50),
            Amount FLOAT,
            Description VARCHAR(255),
            FOREIGN KEY (ICICI_AccountID) REFERENCES ICICI_Accounts(ICICI_AccountID)
        )
    """)
    # Insert data into ICICI tables
    insert_data_into_table(cursor, db_dataframes['ICICI_Accounts.csv'], 'ICICI_Accounts')
    insert_data_into_table(cursor, db_dataframes['ICICI_Transactions.csv'], 'ICICI_Transactions')
    
    # Create HDFC tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HDFC_Accounts (
            HDFC_AccountID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            AccNo VARCHAR(50),
            AccountType VARCHAR(50),
            GovtID VARCHAR(20),
            CurrentBalance FLOAT,
            MonthlyInterest FLOAT,
            LastUpdate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HDFC_Transactions (
            TransactionID INT PRIMARY KEY,
            HDFC_AccountID INT,
            TransDate DATE,
            Type VARCHAR(50),
            TransAmount FLOAT,
            Notes VARCHAR(255),
            FOREIGN KEY (HDFC_AccountID) REFERENCES HDFC_Accounts(HDFC_AccountID)
        )
    """)
    # Insert data into HDFC tables
    insert_data_into_table(cursor, db_dataframes['HDFC_Accounts.csv'], 'HDFC_Accounts')
    insert_data_into_table(cursor, db_dataframes['HDFC_Transactions.csv'], 'HDFC_Transactions')
    
    # Create SBI tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Accounts (
            SBI_AccountID INT PRIMARY KEY,
            AccountHolder VARCHAR(100),
            Acc_Number VARCHAR(50),
            Service_Type VARCHAR(50),
            National_ID VARCHAR(20),
            AmountStored FLOAT,
            Interest_Rate FLOAT,
            Last_Updated DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Transactions (
            TransactionID INT PRIMARY KEY,
            SBI_AccountID INT,
            Date DATE,
            Type_of_Transaction VARCHAR(50),
            Amount FLOAT,
            Details VARCHAR(255),
            FOREIGN KEY (SBI_AccountID) REFERENCES SBI_Accounts(SBI_AccountID)
        )
    """)
    # Insert data into SBI tables
    insert_data_into_table(cursor, db_dataframes['SBI_Accounts.csv'], 'SBI_Accounts')
    insert_data_into_table(cursor, db_dataframes['SBI_Transactions.csv'], 'SBI_Transactions')

    cnx.commit()
    print("Banks database setup completed.")

# Function to setup MutualFunds database
def setup_mutual_funds(db_dataframes):
    # Create MutualFunds and MutualFundRates tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MutualFunds (
            MutualFundID INT PRIMARY KEY,
            FundName VARCHAR(100),
            Category VARCHAR(50),
            RiskProfile VARCHAR(50),
            ManagerName VARCHAR(100)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MutualFundRates (
            RateID INT AUTO_INCREMENT PRIMARY KEY,
            MutualFundID INT,
            RateDate DATE,
            RatePerQuantity FLOAT,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID)
        )
    """)
    # Insert data into MutualFunds and MutualFundRates tables
    insert_data_into_table(cursor, db_dataframes['MutualFunds.csv'], 'MutualFunds')
    insert_data_into_table(cursor, db_dataframes['MutualFundRates.csv'], 'MutualFundRates', include_id=False)
    
    # Create SBI Mutual Fund tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_MF_Clients (
            SBI_ClientID INT PRIMARY KEY,
            FullName VARCHAR(100),
            ClientEmail VARCHAR(100),
            ContactNumber VARCHAR(50),
            PAN_Number VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            RegistrationDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_MF_Returns (
            ReturnID INT PRIMARY KEY,
            MutualFundID INT,
            SBI_ClientID INT,
            InvestmentDate DATE,
            UnitsPurchased FLOAT,
            InvestmentAmount FLOAT,
            PurchaseRate FLOAT,
            CurrentNAV FLOAT,
            CurrentValue FLOAT,
            ReturnPercentage FLOAT,
            LastUpdated DATE,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID),
            FOREIGN KEY (SBI_ClientID) REFERENCES SBI_MF_Clients(SBI_ClientID)
        )
    """)
    # Insert data into SBI Mutual Fund tables
    insert_data_into_table(cursor, db_dataframes['SBI_MF_Clients.csv'], 'SBI_MF_Clients')
    insert_data_into_table(cursor, db_dataframes['SBI_MF_Returns.csv'], 'SBI_MF_Returns')
    
    # Create Tata Mutual Fund tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TataMF_Investors (
            Tata_ClientID INT PRIMARY KEY,
            InvestorName VARCHAR(100),
            EmailAddress VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            ResidentialAddress VARCHAR(255),
            DOB DATE,
            JoinDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TataMF_InvestmentReturns (
            InvestmentReturnID INT PRIMARY KEY,
            MutualFundID INT,
            Tata_ClientID INT,
            DateOfInvestment DATE,
            UnitsBought FLOAT,
            InvestmentINR FLOAT,
            PurchaseRate FLOAT,
            CurrentNAVValue FLOAT,
            InvestmentValue FLOAT,
            GainLossPercentage FLOAT,
            LastUpdated DATE,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID),
            FOREIGN KEY (Tata_ClientID) REFERENCES TataMF_Investors(Tata_ClientID)
        )
    """)
    # Insert data into Tata Mutual Fund tables
    insert_data_into_table(cursor, db_dataframes['TataMF_Investors.csv'], 'TataMF_Investors')
    insert_data_into_table(cursor, db_dataframes['TataMF_InvestmentReturns.csv'], 'TataMF_InvestmentReturns')
    
    # Create Bajaj Mutual Fund tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BajajMF_Customers (
            Bajaj_CustomerID INT PRIMARY KEY,
            Name VARCHAR(100),
            Email VARCHAR(100),
            Mobile VARCHAR(50),
            PAN_Num VARCHAR(20),
            Addr VARCHAR(255),
            DOB DATE,
            DateJoined DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BajajMF_ClientReturns (
            ClientReturnID INT PRIMARY KEY,
            MutualFundID INT,
            Bajaj_CustomerID INT,
            InvestmentDate DATE,
            UnitsPurchased FLOAT,
            AmountInvested FLOAT,
            PurchaseRate FLOAT,
            CurrentNAV FLOAT,
            CurrentValue FLOAT,
            ProfitLossPerc FLOAT,
            UpdateDate DATE,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID),
            FOREIGN KEY (Bajaj_CustomerID) REFERENCES BajajMF_Customers(Bajaj_CustomerID)
        )
    """)
    # Insert data into Bajaj Mutual Fund tables
    insert_data_into_table(cursor, db_dataframes['BajajMF_Customers.csv'], 'BajajMF_Customers')
    insert_data_into_table(cursor, db_dataframes['BajajMF_ClientReturns.csv'], 'BajajMF_ClientReturns')

    cnx.commit()
    print("MutualFunds database setup completed.")

# Function to setup StockPlatforms database
# def setup_stock_platforms(db_dataframes):
#     # Create Zerodha tables
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Zerodha_Clients (
#             Zerodha_ClientID INT PRIMARY KEY,
#             ClientName VARCHAR(100),
#             Email VARCHAR(100),
#             PhoneNumber VARCHAR(50),
#             PAN VARCHAR(20),
#             Address VARCHAR(255),
#             DateOfBirth DATE,
#             AccountCreationDate DATE
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Zerodha_Stocks (
#             Zerodha_StockID INT PRIMARY KEY,
#             StockSymbol VARCHAR(10),
#             StockName VARCHAR(100),
#             Sector VARCHAR(50),
#             Exchange VARCHAR(10)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Zerodha_Orders (
#             OrderID INT PRIMARY KEY,
#             ClientID INT,
#             StockID INT,
#             OrderType VARCHAR(10),
#             Quantity INT,
#             PricePerShare FLOAT,
#             TotalAmount FLOAT,
#             OrderDate DATETIME,
#             OrderStatus VARCHAR(20),
#             FOREIGN KEY (ClientID) REFERENCES Zerodha_Clients(Zerodha_ClientID),
#             FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Zerodha_Stock_Prices (
#             PriceID INT AUTO_INCREMENT PRIMARY KEY,
#             StockID INT,
#             Date DATE,
#             OpenPrice FLOAT,
#             ClosePrice FLOAT,
#             HighPrice FLOAT,
#             LowPrice FLOAT,
#             Volume INT,
#             LastUpdated DATETIME,
#             FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
#         )
#     """)
#     # Insert data into Zerodha tables
#     insert_data_into_table(cursor, db_dataframes['Zerodha_Clients.csv'], 'Zerodha_Clients')
#     insert_data_into_table(cursor, db_dataframes['Zerodha_Stocks.csv'], 'Zerodha_Stocks')
#     insert_data_into_table(cursor, db_dataframes['Zerodha_Orders.csv'], 'Zerodha_Orders')
#     insert_data_into_table(cursor, db_dataframes['Zerodha_Stock_Prices.csv'], 'Zerodha_Stock_Prices', include_id=False)
    
#     # Create Groww tables
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Groww_Clients (
#             Groww_ClientID INT PRIMARY KEY,
#             ClientName VARCHAR(100),
#             Email VARCHAR(100),
#             PhoneNumber VARCHAR(50),
#             PAN VARCHAR(20),
#             Address VARCHAR(255),
#             DateOfBirth DATE,
#             AccountCreationDate DATE
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Groww_Stocks (
#             Groww_StockID INT PRIMARY KEY,
#             Symbol VARCHAR(10),
#             Name VARCHAR(100),
#             Sector VARCHAR(50),
#             Exchange VARCHAR(10)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Groww_Orders (
#             OrderID INT PRIMARY KEY,
#             ClientID INT,
#             StockID INT,
#             Type VARCHAR(10),
#             Quantity INT,
#             Price FLOAT,
#             TotalValue FLOAT,
#             Timestamp DATETIME,
#             Status VARCHAR(20),
#             FOREIGN KEY (ClientID) REFERENCES Groww_Clients(Groww_ClientID),
#             FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Groww_Stock_Prices (
#             PriceID INT AUTO_INCREMENT PRIMARY KEY,
#             StockID INT,
#             Date DATE,
#             Open FLOAT,
#             Close FLOAT,
#             High FLOAT,
#             Low FLOAT,
#             Volume INT,
#             LastUpdated DATETIME,
#             FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
#         )
#     """)
#     # Insert data into Groww tables
#     insert_data_into_table(cursor, db_dataframes['Groww_Clients.csv'], 'Groww_Clients')
#     insert_data_into_table(cursor, db_dataframes['Groww_Stocks.csv'], 'Groww_Stocks')
#     insert_data_into_table(cursor, db_dataframes['Groww_Orders.csv'], 'Groww_Orders')
#     insert_data_into_table(cursor, db_dataframes['Groww_Stock_Prices.csv'], 'Groww_Stock_Prices', include_id=False)
    
#     # Create SBI_Stocks tables
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS SBI_Stocks_Clients (
#             SBI_ClientID INT PRIMARY KEY,
#             ClientName VARCHAR(100),
#             Email VARCHAR(100),
#             PhoneNumber VARCHAR(50),
#             PAN VARCHAR(20),
#             Address VARCHAR(255),
#             DateOfBirth DATE,
#             AccountStartDate DATE
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS SBI_Stocks_List (
#             SBI_StockID INT PRIMARY KEY,
#             StockCode VARCHAR(10),
#             StockName VARCHAR(100),
#             Sector VARCHAR(50),
#             Exchange VARCHAR(10)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS SBI_Stocks_Orders (
#             OrderID INT PRIMARY KEY,
#             ClientID INT,
#             StockID INT,
#             TradeType VARCHAR(10),
#             Quantity INT,
#             PricePerShare FLOAT,
#             TotalValue FLOAT,
#             TradeTimestamp DATETIME,
#             TradeStatus VARCHAR(20),
#             FOREIGN KEY (ClientID) REFERENCES SBI_Stocks_Clients(SBI_ClientID),
#             FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS SBI_Stocks_Prices (
#             PriceID INT AUTO_INCREMENT PRIMARY KEY,
#             StockID INT,
#             Date DATE,
#             Open_Price FLOAT,
#             Close_Price FLOAT,
#             High_Price FLOAT,
#             Low_Price FLOAT,
#             Trade_Volume INT,
#             LastUpdated DATETIME,
#             FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
#         )
#     """)
#     # Insert data into SBI_Stocks tables
#     insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Clients.csv'], 'SBI_Stocks_Clients')
#     insert_data_into_table(cursor, db_dataframes['SBI_Stocks_List.csv'], 'SBI_Stocks_List')
#     insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Orders.csv'], 'SBI_Stocks_Orders')
#     insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Prices.csv'], 'SBI_Stocks_Prices', include_id=False)

#     cnx.commit()
#     print("StockPlatforms database setup completed.")

def setup_stock_platforms(db_dataframes):
    # Create Zerodha tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Clients (
            Zerodha_ClientID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            AccountCreationDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Stocks (
            Zerodha_StockID INT PRIMARY KEY,
            StockSymbol VARCHAR(10),
            StockName VARCHAR(100),
            Sector VARCHAR(50),
            Exchange VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Orders (
            OrderID INT PRIMARY KEY,
            ClientID INT,
            StockID INT,
            OrderType VARCHAR(10),
            Quantity INT,
            PricePerShare FLOAT,
            TotalAmount FLOAT,
            OrderDate DATETIME,
            OrderStatus VARCHAR(20),
            FOREIGN KEY (ClientID) REFERENCES Zerodha_Clients(Zerodha_ClientID),
            FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Stock_Prices (
            PriceID INT AUTO_INCREMENT PRIMARY KEY,
            StockID INT,
            Date DATE,
            OpenPrice FLOAT,
            ClosePrice FLOAT,
            HighPrice FLOAT,
            LowPrice FLOAT,
            Volume INT,
            LastUpdated DATETIME,
            FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
        )
    """)
    # Insert data into Zerodha tables
    insert_data_into_table(cursor, db_dataframes['Zerodha_Clients.csv'], 'Zerodha_Clients')
    insert_data_into_table(cursor, db_dataframes['Zerodha_Stocks.csv'], 'Zerodha_Stocks')
    insert_data_into_table(cursor, db_dataframes['Zerodha_Orders.csv'], 'Zerodha_Orders')
    
    # Insert Stock_Prices with include_id=True
    zerodha_prices_df = db_dataframes['Zerodha_Stock_Prices.csv']
    print("Zerodha_Stock_Prices DataFrame columns:", zerodha_prices_df.columns)
    print("Zerodha_Stock_Prices DataFrame sample:", zerodha_prices_df.head())
    print("Zerodha_Stock_Prices 'StockID' null count:", zerodha_prices_df['StockID'].isnull().sum())
    insert_data_into_table(cursor, zerodha_prices_df, 'Zerodha_Stock_Prices', include_id=True)
    
    # Create Groww tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Clients (
            Groww_ClientID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            AccountCreationDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Stocks (
            Groww_StockID INT PRIMARY KEY,
            Symbol VARCHAR(10),
            Name VARCHAR(100),
            Sector VARCHAR(50),
            Exchange VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Orders (
            OrderID INT PRIMARY KEY,
            ClientID INT,
            StockID INT,
            Type VARCHAR(10),
            Quantity INT,
            Price FLOAT,
            TotalValue FLOAT,
            Timestamp DATETIME,
            Status VARCHAR(20),
            FOREIGN KEY (ClientID) REFERENCES Groww_Clients(Groww_ClientID),
            FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Stock_Prices (
            PriceID INT AUTO_INCREMENT PRIMARY KEY,
            StockID INT,
            Date DATE,
            Open FLOAT,
            Close FLOAT,
            High FLOAT,
            Low FLOAT,
            Volume INT,
            LastUpdated DATETIME,
            FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
        )
    """)
    # Insert data into Groww tables
    insert_data_into_table(cursor, db_dataframes['Groww_Clients.csv'], 'Groww_Clients')
    insert_data_into_table(cursor, db_dataframes['Groww_Stocks.csv'], 'Groww_Stocks')
    insert_data_into_table(cursor, db_dataframes['Groww_Orders.csv'], 'Groww_Orders')
    
    # Insert Stock_Prices with include_id=True
    groww_prices_df = db_dataframes['Groww_Stock_Prices.csv']
    print("Groww_Stock_Prices DataFrame columns:", groww_prices_df.columns)
    print("Groww_Stock_Prices DataFrame sample:", groww_prices_df.head())
    print("Groww_Stock_Prices 'StockID' null count:", groww_prices_df['StockID'].isnull().sum())
    insert_data_into_table(cursor, groww_prices_df, 'Groww_Stock_Prices', include_id=True)
    
    # Create SBI_Stocks tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_Clients (
            SBI_ClientID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            AccountStartDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_List (
            SBI_StockID INT PRIMARY KEY,
            StockCode VARCHAR(10),
            StockName VARCHAR(100),
            Sector VARCHAR(50),
            Exchange VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_Orders (
            OrderID INT PRIMARY KEY,
            ClientID INT,
            StockID INT,
            TradeType VARCHAR(10),
            Quantity INT,
            PricePerShare FLOAT,
            TotalValue FLOAT,
            TradeTimestamp DATETIME,
            TradeStatus VARCHAR(20),
            FOREIGN KEY (ClientID) REFERENCES SBI_Stocks_Clients(SBI_ClientID),
            FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_Prices (
            PriceID INT AUTO_INCREMENT PRIMARY KEY,
            StockID INT,
            Date DATE,
            Open_Price FLOAT,
            Close_Price FLOAT,
            High_Price FLOAT,
            Low_Price FLOAT,
            Trade_Volume INT,
            LastUpdated DATETIME,
            FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
        )
    """)
    # Insert data into SBI_Stocks tables
    insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Clients.csv'], 'SBI_Stocks_Clients')
    insert_data_into_table(cursor, db_dataframes['SBI_Stocks_List.csv'], 'SBI_Stocks_List')
    insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Orders.csv'], 'SBI_Stocks_Orders')
    
    # Insert Stock_Prices with include_id=True
    sbi_prices_df = db_dataframes['SBI_Stocks_Prices.csv']
    print("SBI_Stocks_Prices DataFrame columns:", sbi_prices_df.columns)
    print("SBI_Stocks_Prices DataFrame sample:", sbi_prices_df.head())
    print("SBI_Stocks_Prices 'StockID' null count:", sbi_prices_df['StockID'].isnull().sum())
    insert_data_into_table(cursor, sbi_prices_df, 'SBI_Stocks_Prices', include_id=True)

    cnx.commit()
    print("StockPlatforms database setup completed.")


# Function to insert data into a table
def insert_data_into_table(cursor, df, table_name, include_id=True):
    # Prepare column names and placeholders
    columns = df.columns.tolist()
    if not include_id:
        columns = columns[1:]  # Skip the first column (auto-increment ID)
    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join(columns)
    insert_stmt = f"INSERT INTO {table_name} ({columns_formatted}) VALUES ({placeholders})"
    data_tuples = df[columns].apply(tuple, axis=1).tolist()
    cursor.executemany(insert_stmt, data_tuples)
    print(f"Inserted data into '{table_name}'.")

# Setup each database
for db_name in databases:
    setup_database(db_name)

# Close cursor and connection
cursor.close()
cnx.close()
print("Data insertion completed and connection closed.")
